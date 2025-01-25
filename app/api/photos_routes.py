from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..server import Base, engine, Photo

app = Flask(__name__)

@app.route('/create', methods=['POST'])
def create_photo():

    data = request.get_json()


    if not data in data:
        return jsonify({"error": "Invalid input"}), 400

    try:

        with Session(engine) as session:

            new_photo = Photo(
                photo_file_name=data['photo_file_name'],
                date_modified=data['date_modified'],
                date_created=data['date_created'],
                is_deleted=data['is_deleted']
            )
            session.add(new_photo)
            session.commit()
            session.refresh(new_photo)

            # Return success response
            return jsonify({
                "id": new_photo.id,
                "message": "New photo created successfully"
            }), 201
    except SQLAlchemyError as e:
        # Otherwise return error
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
