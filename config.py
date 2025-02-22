import os
from dotenv import load_dotenv

# Memuat file .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('APP_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
