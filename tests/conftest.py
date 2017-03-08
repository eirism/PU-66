import pytest
import os
from tempfile import mkstemp
from flask_socketio import SocketIOTestClient


@pytest.fixture(scope="session")
def app():
    old_dburl = os.environ.get('DATABASE_URL', '')
    fd, filename = mkstemp(suffix='.db', prefix='test_', dir='tmp')
    os.environ['DATABASE_URL'] = 'sqlite:///' + filename
    from iris import app as _app
    import db_create
    db_create.create_db()
    import db_upgrade
    db_upgrade.upgrade_db()
    yield _app
    os.environ['DATABASE_URL'] = old_dburl
    os.close(fd)
    os.remove(filename)


@pytest.fixture(scope="function")
def client_socketio(app):
    from iris import socketio
    return SocketIOTestClient(app, socketio)


@pytest.fixture(scope="session")
def db(app):
    from iris import db
    return db


@pytest.fixture(scope="function")
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    db.session = session
    yield session
    transaction.rollback()
    connection.close()
    session.remove()
