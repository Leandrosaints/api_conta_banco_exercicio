import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'banco.db')
SQLALCHEMY_TRACK_MODIFICATION = True

DEBUG = True

JWT_SECRET_KEY = 'super-secret'
JWT_BLACKLIST_ENABLED = True


