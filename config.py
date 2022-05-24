import os
from datetime import timedelta



basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'banco.db')
SQLALCHEMY_TRACK_MODIFICATION = True

DEBUG = True

JWT_SECRET_KEY = 'super-secret'
JWT_BLACKLIST_ENABLED = True
class Config_token(object):
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=30)
    
        
   


#JWT_REFRESH_TOKEN_EXPIRES  = timedelta(days=30)


