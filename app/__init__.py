"""Flask application factory"""
from flask import Flask
from flask_cors import CORS
from database import db, init_db
from config import get_config

def create_app(config=None):
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    if config is None:
        config = get_config()
    app.config.from_object(config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Initialize database
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp)
    
    return app
