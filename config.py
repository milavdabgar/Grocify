import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    
    
class mySQLapp(Config):
    import urllib.parse
    
    mysql_host = os.environ.get('DB_HOST')
    mysql_user = os.environ.get('DB_USER')
    mysql_password = os.environ.get('DB_PASSWORD')
    mysql_database = os.environ.get('DB_DATABASE')   
    mysql_encoded_password = urllib.parse.quote_plus(mysql_password)
    
    # MySQL connection for sqlAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
    f'mysql+mysqlconnector://root:{mysql_encoded_password}@localhost/grocify_sample'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
     
    # MySQL connection for raw SQL
    db_config = {
        'host': mysql_host,
        'user': mysql_user,
        'password': mysql_password,
        'database': mysql_database
    }