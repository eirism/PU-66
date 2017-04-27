"""Fixtures for pytest."""

import pytest
import os
from tempfile import mkstemp
from flask_socketio import SocketIOTestClient


@pytest.fixture(scope="session")
def app():
    """
    Set up the app.

    Creates a temporary DB.
    """
    old_dburl = os.environ.get('DATABASE_URL', '')
    if not os.path.isdir('tmp'):
        os.mkdir('tmp')
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
    """A test client for socketIO."""
    from iris import socketio
    return SocketIOTestClient(app, socketio)


@pytest.fixture(scope="session")
def db(app):
    """The DB object."""
    from iris import db
    return db


@pytest.fixture(scope="function", autouse=True)
def session(db, monkeypatch):
    """
    Prevent the session from being committed.

    Will roll back the changes on teardown.
    """
    remove = db.session.remove
    monkeypatch.setattr(db.session, 'commit', db.session.flush)
    monkeypatch.setattr(db.session, 'remove', lambda: None)
    yield db.session
    remove()


@pytest.fixture(scope="function")
def logged_in_user(monkeypatch):
    """Create  a default user, and sets current_user to it."""
    from iris import user_datastore
    default_user = user_datastore.create_user(email="defaul@example.com", password="default")
    monkeypatch.setattr('iris.views.current_user', default_user)
    monkeypatch.setattr('flask_login.current_user', default_user)
    return default_user


@pytest.fixture()
def create_default_course(session):
    from iris import user_datastore
    course = user_datastore.create_role(code="TDT4140", name="PU")
    session.commit()
    yield course
