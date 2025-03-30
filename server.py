import os
from flask import Flask
from flask_cors import CORS
from app.api.photos_routes import photo_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Set configuration for all Blueprints to use
    app.config["PHOTOS_FOLDER"] = os.path.join(os.path.expanduser("~"), "photo-frame", "photos")

    # Ensure directory exists before running
    os.makedirs(app.config["PHOTOS_FOLDER"], exist_ok=True)

    # Register blueprints
    app.register_blueprint(photo_bp, url_prefix="/api/photos")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)
