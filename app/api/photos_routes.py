import os
from flask import Flask, request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, func
from server import engine, Photo, Base
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  #This will allow any frontend to talk to the flask backend

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


            photo.is_deleted=True, #set to True
            photo.date_modified=func.now(), #Update the timestamp
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
    if not data or 'photo_file_name' not in data:
        return jsonify({"error": "Invalid input"}), 400

    try:

        with Session(engine) as session:
            new_photo = Photo(photo_file_name=data["photo_file_name"])
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
