"""Contains config variables."""
import os

basedir = os.path.abspath(os.path.dirname(__file__))

PORT = int(os.environ.get('PORT', 5000))
SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-for-production')
DEBUG = os.environ.get('DEBUG', 0)
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG_TB_INTERCEPT_REDIRECTS = False
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = SECRET_KEY
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_SEND_PASSWORD_EMAIL = False

BUTTON_ACTIONS = [
    ['slow', 'Slow'],
    ['fast', 'Fast'],
    ['easy', 'Easy'],
    ['hard', 'Hard']
]
