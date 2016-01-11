import os
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(basedir, 'data.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


DEBUG = False
SQLALCHEMY_ECHO = False

# test
