


import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGIN_VIEW = 'admin.login'
    LOGIN_MESSAGE_CATEGORY = 'info'
    SITE_NAME = 'myTemplates'
    SITE_TAGLINE = 'Premium Digital Templates'
    SITE_URL = os.environ.get('SITE_URL', 'http://localhost:5000')




