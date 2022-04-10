from os import environ, path
from dotenv import load_dotenv

DB_NAME = "main"

class Config:
    """Base config."""
    #SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    MAX_CONTENT_LENGTH = 16*1000*1000
    RECEIPT_FOLDER = '..\\uploads\\receipts'
    IMPORT_FOLDER = '..\\uploads\\imports'
    UPLOAD_FOLDER = '..\\uploads'
    EXPORT_FOLDER = '\\uploads\\exports'
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.pdf', '.csv', '.xls', '.xlsx']
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

class ProdConfig(Config):
    basedir = path.abspath(path.dirname(__file__))
    load_dotenv('/home/sai/.env')
    env_dict = dict(environ)
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI')
    SECRET_KEY = environ.get('SECRET_KEY')
    SERVER_NAME = environ.get('SERVER_NAME')
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_TIME_LIMIT = 600

class DevConfig(Config):
    basedir = path.abspath(path.dirname(__file__))
    load_dotenv('C:\saiscripts\intercept_branch\Payment Web App Project\.env')
    env_dict = dict(environ)
    FLASK_ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')
    SECRET_KEY = environ.get('SECRET_KEY')
    
class ProdTestConfig(DevConfig):
    '''
    Developer config settings but production database server
    '''
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI')

if __name__ == '__main__':
    print(environ.get('SQLALCHEMY_DATABASE_URI'))