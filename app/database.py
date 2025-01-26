from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Inisialisasi SQLAlchemy
db = SQLAlchemy()

# Fungsi untuk menginisialisasi database
def init_db(app):
    app.config.from_object('config.Config')  # Mengambil konfigurasi dari config.py
    db.init_app(app)

# Cek koneksi ke database
def test_db_connection():
    try:
        # Pastikan menggunakan 'text()' untuk ekspresi SQL
        db.session.execute(text("SELECT 1"))
        return "Connection successful"
    except Exception as e:
        return {"error": str(e), "message": "Connection failed"}