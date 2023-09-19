import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    DEBUG = True
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = False

    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SECURITY_PASSWORD_HASH = os.environ.get("SECURITY_PASSWORD_HASH") or "bcrypt"
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT") or "super secret"
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    WTF_CSRF_ENABLED = False


class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "instance")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        SQLITE_DB_DIR, "grocify.sqlite"
    )
    DEBUG = True


class TestingConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "instance")
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    DEBUG = True


class ProductionConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "instance")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        SQLITE_DB_DIR, "app_prod.sqlite3"
    )
    DEBUG = False


class mySQLapp(LocalDevelopmentConfig):
    import urllib.parse

    mysql_host = os.environ.get("DB_HOST")
    mysql_user = os.environ.get("DB_USER")
    mysql_password = os.environ.get("DB_PASSWORD")
    mysql_database = os.environ.get("DB_DATABASE")
    mysql_encoded_password = urllib.parse.quote_plus(mysql_password)

    # MySQL connection for sqlAlchemy
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://root:{mysql_encoded_password}@localhost/grocify_sample"
    )

    # MySQL connection for raw SQL
    db_config = {
        "host": mysql_host,
        "user": mysql_user,
        "password": mysql_password,
        "database": mysql_database,
    }
