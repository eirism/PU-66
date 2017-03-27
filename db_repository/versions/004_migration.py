from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
role = Table('role', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=80)),
    Column('description', VARCHAR(length=255)),
)

roles_users = Table('roles_users', pre_meta,
    Column('user_id', INTEGER),
    Column('role_id', INTEGER),
)

course = Table('course', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('code', String(length=20)),
    Column('name', String(length=80)),
    Column('description', String(length=255)),
)

courses_users = Table('courses_users', post_meta,
    Column('user_id', Integer),
    Column('course_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['role'].drop()
    pre_meta.tables['roles_users'].drop()
    post_meta.tables['course'].create()
    post_meta.tables['courses_users'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['role'].create()
    pre_meta.tables['roles_users'].create()
    post_meta.tables['course'].drop()
    post_meta.tables['courses_users'].drop()
