from .photos_routes import photos_bp

def register_api_blueprints(app):
    """Register API blueprints"""
    app.register_blueprint(photos_bp, url_prefix="/api/photos")
