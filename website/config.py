from os import environ, path
from dotenv import load_dotenv

DB_NAME = "main"

class Config:
    """Base config."""
    #SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    MAX_CONTENT_LENGTH = 16*1000*1000
    RECEIPT_FOLDER = '..\\assets\\receipts'
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.pdf']
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

class ProdConfig(Config):
    basedir = path.abspath(path.dirname(__file__))
    load_dotenv('/home/sai/.env')
    env_dict = dict(environ)
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQL_ALCHEMY_DATABASE_URI = env_dict['PROD_DATABASE_URI']
    SECRET_KEY = env_dict['SECRET_KEY']

class DevConfig(Config):
    basedir = path.abspath(path.dirname(__file__))
    load_dotenv('C:\saiscripts\intercept_branch\Payment Web App Project\.env')
    env_dict = dict(environ)
    FLASK_ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = env_dict['DEV_DATABASE_URI']
    SECRET_KEY = env_dict['SECRET_KEY']

if __name__ == '__main__':
    print(environ.get('SQLALCHEMY_DATABASE_URI'))