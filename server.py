import os
from flask import Flask
from app.api import register_api_blueprints
from app.db.database import db, Base, engine
from app.models import photos  # Make sure all models are imported so they're registered

def create_app():
    app = Flask(__name__)

    # configure the SQLite database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

    # initialize the app with the extension
    db.init_app(app)

    # Set configuration for all Blueprints to use
    app.config["PHOTOS_FOLDER"] = os.path.join(os.path.expanduser("~"), "photo-frame", "photos")

    # Ensure directory exists before running
    os.makedirs(app.config["PHOTOS_FOLDER"], exist_ok=True)

    # Now that models are imported, create the tables
    with app.app_context():
        db.create_all()

    # Register blueprints
    register_api_blueprints(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)
