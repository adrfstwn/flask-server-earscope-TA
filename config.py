import os
from dotenv import load_dotenv

# Memuat file .env
load_dotenv()

class Config:
    # Ambil URI database dari file .env
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
