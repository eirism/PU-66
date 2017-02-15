import os
basedir = os.path.abspath(os.path.dirname(__file__))

PORT = int(os.environ['PORT'])
SECRET_KEY = os.environ['SECRET_KEY']
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
