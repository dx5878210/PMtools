#!flask/bin/python
import sys
sys.path.append('..')
from migrate.versioning import api
from config.default import SQLALCHEMY_MIGRATE_REPO
from config.default import SQLALCHEMY_DATABASE_URI
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
print('Current database version:' + str(v))
