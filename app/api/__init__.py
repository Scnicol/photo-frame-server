from flask import Blueprint
from .photos_routes import photo_bp

def register_api_blueprints(app):
    """Register API blueprints"""
    app.register_blueprint(photo_bp, url_prefix="/api/photos")
