from flask import Flask
from .database import init_db    
from .routes import bp

def earscope_app():
    app = Flask(__name__)

    # Inisialisasi database
    init_db(app)

    # Registrasi blueprint untuk routes
    app.register_blueprint(bp)

    return app
