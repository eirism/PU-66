from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
questions = Table('questions', post_meta,
    Column('question_id', Integer, primary_key=True, nullable=False),
    Column('session_id', Integer),
    Column('question', Text),
    Column('timestamp', DateTime),
    Column('answered', Boolean, default=ColumnDefault(False)),
    Column('flagged', Boolean, default=ColumnDefault(False)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['questions'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['questions'].drop()
