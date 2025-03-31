import os, base64, uuid,random
from flask import Flask, request, jsonify, send_from_directory, Blueprint
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, func
from app.models.photos import engine, Photo, Base
from flask_cors import CORS, cross_origin

# Creat a Blueprint for photos
photo_bp = Blueprint("photos", __name__)

# Set the upload directory inside the current user's home directory
PHOTOS_FOLDER = os.path.join(os.path.expanduser("~"), "photo-frame", "photos")

# Ensure the directory exists
os.makedirs(PHOTOS_FOLDER, exist_ok=True)

@photo_bp.route('/random-photo', methods=['GET'])
@cross_origin()
def get_random_photo():
    try:
        with Session(engine) as session:
            #Select a random row that isn't deleted
            stmt = select(Photo).where(Photo.is_deleted == False).order_by(func.random()).limit(1)
            photo = session.scalar(stmt)

            #if there are no photos return error
            if not photo:
                return jsonify({"error": "No available photos"}), 404

            #Here find the file path of the photo
            file_path = os.path.join(PHOTOS_FOLDER, photo.photo_file_name)

            #Then make sure the file exists
            if not os.path.exists(file_path):
                return jsonify({"error": "Photo file not found on server"}), 500


            return send_from_directory(PHOTOS_FOLDER, photo.photo_file_name, as_attachment=False)


    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@photo_bp.route('/delete/<int:photo_id>', methods=['DELETE'])
@cross_origin()
def delete_photo(photo_id):
    try:
        with Session(engine) as session:
            
            #Fetch the photo by ID
            photo = session.get(Photo, photo_id)

            #Create Error if the photo cannot be found
            if not photo:
                return jsonify({"error": "Photo not found"}), 404

            #Check if it has already been deleted, return success and don't change anything
            if photo.is_deleted:
                return jsonify({
                    "id": photo.id,
                    "message": "Photo is already deleted"
                }), 200

            #Here we will store file path
            file_path = os.path.join(PHOTOS_FOLDER, photo.photo_file_name)

            photo.is_deleted=True #set to True
            photo.photo_file_name=None #Null out file name



            #here we will delete the file from the system using the saved filepath if it exists
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted photo: {file_path}")

            session.commit()

            return jsonify({
                "id": photo.id,
                "message": "Photo deleted successfully"
            }), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@photo_bp.route('/create', methods=['POST'])
@cross_origin()
def create_photo():

    #Checking if the request has the file part
    if 'imageData' not in request.files:
        return jsonify({"error": "No image file found in request"}), 400

    file = request.files['imageData']

    try:

        # generate a random UUID for the filename
        file_name = f"{uuid.uuid4()}.jpg"

        # generate full path to where the image will be stored in the file system using the UUID
        file_path = os.path.join(PHOTOS_FOLDER, file_name)

        #save the file directly to the file system
        file.save(file_path)

        with Session(engine) as session:
            # set the UUID as the photo_file_name
            new_photo = Photo(photo_file_name=file_name)
            session.add(new_photo)
            session.commit()
            session.refresh(new_photo)

            return jsonify({
                "id": new_photo.id,
                "photo_file_name": new_photo.photo_file_name,
                "date_created": new_photo.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                "date_modified": new_photo.date_modified.strftime("%Y-%m-%d %H:%M:%S"),
                "is_deleted": new_photo.is_deleted,
                "message": "New photo created successfully"
            }), 201
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
