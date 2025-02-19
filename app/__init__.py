from flask import Flask
from flask_socketio import SocketIO
from .database import init_db
from .routes import bp, register_socketio_events
import os

def earscope_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('APP_KEY', 'default_secret_key')  # Default key jika tidak ada env
    socketio = SocketIO(app)

    # Inisialisasi database
    init_db(app)

    # Registrasi blueprint untuk routes
    app.register_blueprint(bp)

    # Registrasi event WebSocket
    register_socketio_events(socketio)

    return app, socketio