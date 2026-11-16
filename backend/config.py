import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.path.join(INSTANCE_DIR, 'srs_review.db')

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{DB_PATH}')
SQLALCHEMY_TRACK_MODIFICATIONS = False

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
