import os, uuid
from datetime import datetime
from flask import request, jsonify, send_from_directory, Blueprint, current_app
from sqlalchemy import select, func
from app.models.photos import Photo
from app.db.database import db

# Create a Blueprint for photos
photos_bp = Blueprint("photos", __name__)

@photos_bp.route("/<int:photo_id>/image", methods=["GET"])
def get_photo_image(photo_id):
    # Fetch the photo by ID
    photo = db.session.get(Photo, photo_id)

    if not photo or photo.is_deleted:
        return jsonify({"error": "Photo not found"}), 404

    # Build file path
    file_path = os.path.join(current_app.config["PHOTOS_FOLDER"], photo.photo_file_name)

    if not os.path.exists(file_path):
        return jsonify({"error": "Photo file not found on server"}), 500

    return send_from_directory(current_app.config["PHOTOS_FOLDER"], photo.photo_file_name, as_attachment=False)

@photos_bp.route("/random", methods=["GET"])
def get_random_photo():
    # Select a random row that isn't deleted
    stmt = select(Photo).where(Photo.is_deleted == False).order_by(func.random()).limit(1)
    photo = db.session.scalar(stmt)

    # If there are no photos return error
    if not photo:
        return jsonify({"error": "No available photos"}), 404

    # Create the file path to the photo
    file_path = os.path.join(current_app.config["PHOTOS_FOLDER"], photo.photo_file_name)

    # Make sure the file exists
    if not os.path.exists(file_path):
        return jsonify({"error": "Photo file not found on server"}), 500

    return send_from_directory(current_app.config["PHOTOS_FOLDER"], photo.photo_file_name, as_attachment=False)

@photos_bp.route("/", methods=["POST"])
def create_photo():
    # Check if the request has the file part
    if "imageData" not in request.files:
        return jsonify({"error": "No image file found in request"}), 400

    file = request.files["imageData"]

    # Generate a random UUID for the filename
    file_name = f"{uuid.uuid4()}.jpg"

    # Generate full path to where the image will be stored in the file system using the UUID
    file_path = os.path.join(current_app.config["PHOTOS_FOLDER"], file_name)

    # Save the file directly to the file system
    file.save(file_path)

    # Set the UUID as the photo_file_name
    new_photo = Photo(photo_file_name=file_name)
    db.session.add(new_photo)
    db.session.commit()
    db.session.refresh(new_photo)

    return jsonify(new_photo.to_dict()), 201

@photos_bp.route("/<int:photo_id>", methods=["DELETE"])
def delete_photo(photo_id):
    # Fetch the photo by ID
    photo = db.session.get(Photo, photo_id)

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
    db.session.commit()

    return jsonify({"message": "Photo deleted successfully"}), 200

@photos_bp.route("/metadata", methods=["GET"])
def get_photo_metadata():
    modified_since = request.args.get("modified_since")

    if modified_since:
        try:
            modified_date = datetime.fromisoformat(modified_since)
            query = db.session.query(Photo).filter(Photo.date_modified > modified_date)
        except ValueError:
            return jsonify({"error": "Invalid date format. Use ISO format (e.g., 2024-04-27T12:00:00)"}), 400
    else:
        query = db.session.query(Photo).filter(Photo.is_deleted == False)

    photos = query.all()
    return jsonify([photo.to_dict() for photo in photos]), 200
