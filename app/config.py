# app/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///tango_dj.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
