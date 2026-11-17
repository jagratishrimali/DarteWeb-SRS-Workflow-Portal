import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.path.join(INSTANCE_DIR, 'srs_review.db')

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

if not SQLALCHEMY_DATABASE_URI and os.environ.get('DB_NAME'):
    db_user = quote_plus(os.environ.get('DB_USER', 'root'))
    db_password = quote_plus(os.environ.get('DB_PASSWORD', ''))
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '3306')
    db_name = os.environ['DB_NAME']
    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    )

if not SQLALCHEMY_DATABASE_URI:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'

SQLALCHEMY_TRACK_MODIFICATIONS = False

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
