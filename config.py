from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Set Flask configuration variables from .env file."""

    # General Flask Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_ENV = environ.get('FLASK_ENV')
    FLASK_APP = 'wsgi.py'
    FLASK_DEBUG = 1
    FLASK_SERVER = environ.get('POS_SERVER')
    FLASK_PORT = environ.get('POS_PORT')
    
    # Point of Sale Config
    POS_MULTIPLE = environ.get('POS_MULTIPLE')
    POS_ID = environ.get('POS_ID')
    
    
    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redemption
    RDM_SERVER = environ.get('RDM_SERVER')
    RDM_PORT = environ.get('RDM_PORT')
    RDM_DB_NAME = environ.get('RDM_DB_NAME')
    RDM_APP_EMAIL = environ.get('RDM_APP_EMAIL')
    RDM_APP_PASSWORD = environ.get('RDM_APP_PASSWORD')