# app/__init__.py
from flask import Flask
from app.extensions import db
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Import models
    with app.app_context():
        from app import models

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.song import song_bp
    from app.routes.orchestra import orchestra_bp
    from app.routes.singer import singer_bp
    from app.routes.tanda import tanda_bp
    from app.routes.playlist import playlist_bp
    # Include user_bp if implementing authentication

    app.register_blueprint(main_bp)
    app.register_blueprint(song_bp, url_prefix='/songs')
    app.register_blueprint(orchestra_bp, url_prefix='/orchestras')
    app.register_blueprint(singer_bp, url_prefix='/singers')
    app.register_blueprint(tanda_bp, url_prefix='/tandas')
    app.register_blueprint(playlist_bp, url_prefix='/playlists')
    # app.register_blueprint(user_bp, url_prefix='/users')  # Optional

    return app
