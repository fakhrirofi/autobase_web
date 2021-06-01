from dotenv import load_dotenv
import os

load_dotenv(".env")
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "SECRET123SECRET123"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REGISTER_TOKEN = os.environ.get('REGISTER_TOKEN') or "SECRET123SECRET123"

    if 'postgres:' in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres', 'postgresql')
