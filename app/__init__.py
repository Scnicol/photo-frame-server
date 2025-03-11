from flask import Flask
from app.api import register_api_blueprints

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)

    # Register blueprints
    register_api_blueprints(app)

    return app
