import os
basedir = os.path.abspath(os.path.dirname(__file__))

PORT = int(os.environ.get('PORT', 5000))
SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-for-production')
DEBUG = os.environ.get('DEBUG', 0)
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

BUTTON_ACTIONS = [
    ['action_slow', 'To slow'],
    ['action_fast', 'To fast'],
    ['action_easy', 'This is easy'],
    ['action_hard', 'This is hard']
]
