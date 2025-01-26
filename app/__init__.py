from flask import Flask
from .database import init_db

def earscope_app():
    app = Flask(__name__)

    # Inisialisasi database
    init_db(app)

    # Registrasi blueprint untuk routes
    from .routes import bp
    app.register_blueprint(bp)

    return app
