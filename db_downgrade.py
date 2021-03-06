"""Utility for downgrading the DB."""
# From: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

from migrate.versioning import api

from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO


def downgrade_db():
    """Downgrade the DB."""
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print('Current database version: ' + str(v))


if __name__ == '__main__':
    downgrade_db()
