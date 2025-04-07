import os, uuid
from flask import request, jsonify, send_from_directory, Blueprint, current_app
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.photos import engine, Photo

#TODO Change all the single quotes to double quotes where needed.
#TODO Check all the comments and add a space and capitalize

# Create a Blueprint for photos
photos_bp = Blueprint("photos", __name__)

@photos_bp.route('/random', methods=['GET']) #TODO update shortcuts to fit new url
def get_random_photo():
    with Session(engine) as session:
        # Select a random row that isn't deleted
        stmt = select(Photo).where(Photo.is_deleted == False).order_by(func.random()).limit(1)
        photo = session.scalar(stmt)

        # If there are no photos return error
        if not photo:
            return jsonify({"error": "No available photos"}), 404

        # Create the file path to the photo
        file_path = os.path.join(current_app.config["PHOTOS_FOLDER"], photo.photo_file_name)

        # Make sure the file exists
        if not os.path.exists(file_path):
            return jsonify({"error": "Photo file not found on server"}), 500

        return send_from_directory(current_app.config["PHOTOS_FOLDER"], photo.photo_file_name, as_attachment=False)

@photos_bp.route('/', methods=['POST']) #TODO update the shortcut
def create_photo():
    # Check if the request has the file part
    if 'imageData' not in request.files:
        return jsonify({"error": "No image file found in request"}), 400

    file = request.files['imageData']

    # Generate a random UUID for the filename
    file_name = f"{uuid.uuid4()}.jpg"

    # Generate full path to where the image will be stored in the file system using the UUID
    file_path = os.path.join(current_app.config["PHOTOS_FOLDER"], file_name)

    # Save the file directly to the file system
    file.save(file_path)

    with Session(engine) as session:
        # Set the UUID as the photo_file_name
        new_photo = Photo(photo_file_name=file_name)
        session.add(new_photo)
        session.commit()
        session.refresh(new_photo)

        return jsonify(new_photo.to_dict()), 201

@photos_bp.route('/<int:photo_id>', methods=['DELETE']) #TODO update the shortcut
def delete_photo(photo_id):
    with Session(engine) as session:
        # Fetch the photo by ID
        photo = session.get(Photo, photo_id)

        # Create Error if the photo cannot be found
        if not photo:
            return jsonify({"error": "Photo not found"}), 404

        # Check if it has already been deleted
        if photo.is_deleted:
            return jsonify({"message": "Photo is already deleted"}), 200

        # Delete the file from the system using the saved filepath if it exists
        file_path = os.path.join(current_app.config["PHOTOS_FOLDER"], photo.photo_file_name)
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted photo: {file_path}")

        # Update photo database entry
        photo.is_deleted = True
        photo.photo_file_name = None
        session.commit()

        return jsonify({"message": "Photo deleted successfully"}), 200
