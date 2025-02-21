import os, base64, uuid
from flask import Flask, request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, func
from server import engine, Photo, Base
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  #This will allow any frontend to talk to the flask backend

# Set the upload directory inside the current user's home directory
PHOTOS_FOLDER = os.path.join(os.path.expanduser("~"), "photo-frame", "photos")
app.config['PHOTOS_FOLDER'] = PHOTOS_FOLDER

# Ensure the directory exists
os.makedirs(app.config['PHOTOS_FOLDER'], exist_ok=True)

@app.route('/random-photo', methods=['GET'])
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

            #Read the file and encode it as Base64
            with open(file_path, "rb") as image_file:
                base64_encoded = base64.b64encode(image_file.read()).decode("utf-8")

            return jsonify({
                "id": photo.id,
                "photo_file_name": photo.photo_file_name,
                "date_created": photo.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                "image_data": base64_encoded #this should be the encoded image data
            }), 200


    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route('/delete/<int:photo_id>', methods=['DELETE'])
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


            photo.is_deleted=True #set to True
                #Timestamp should be updated in the model file
            photo.photo_file_name=None #Null out file name

            session.commit()

            #here we will delete the file from the system using the saved filepath if it exists

            return jsonify({
                "id": photo.id,
                "message": "Photo deleted successfully"
            }), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route('/create', methods=['POST'])
@cross_origin()
def create_photo():
    data = request.get_json()

    # Make sure the data is there before creating
    if not data or 'image_data' not in data:
        return jsonify({"error": "Invalid input"}), 400


    try:

        # extract image data from the data dictionary and convert base64 image data into binary data
        image_data = base64.b64decode(data["image_data"])

        # generate a random UUID for the filename
        file_name = f"{uuid.uuid4()}.jpg"

        # generate full path to where the image will be stored in the file system using the UUID
        file_path = os.path.join(PHOTOS_FOLDER, file_name)

        # write the image binary to that full path
        with open(file_path, "wb") as image_file:
            image_file.write(image_data)

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

if __name__ == '__main__':
    app.run(debug=True)
