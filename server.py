import os
from flask import Flask
from flask_cors import CORS
from app.api import register_api_blueprints

#TODO Refactor Project layout to follow the Flask tutorials' layout as close as possible

def create_app():
    app = Flask(__name__)

    # Set configuration for all Blueprints to use
    app.config["PHOTOS_FOLDER"] = os.path.join(os.path.expanduser("~"), "photo-frame", "photos")

    # Ensure directory exists before running
    os.makedirs(app.config["PHOTOS_FOLDER"], exist_ok=True)

    # Register blueprints
    register_api_blueprints(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)
