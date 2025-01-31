from flask import Flask, request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from server import engine, Photo, Base
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  #This will allow any frontend to talk to the flask backend

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
