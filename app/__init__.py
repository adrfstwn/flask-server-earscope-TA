from flask import Flask
from flask_socketio import SocketIO
from .routes import bp, register_socketio_events
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Inisialisasi database
    from app import models
    db.init_app(app)
    
    # Setup Migrate 
    migrate.init_app(app, db)
    
    # Setup WebSocket
    socketio.init_app(app)

    # Registrasi blueprint untuk routes
    app.register_blueprint(bp)

    # Registrasi event WebSocket
    register_socketio_events(socketio)

    return app
