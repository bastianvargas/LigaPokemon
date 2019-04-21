import os

PWD = os.path.abspath(os.curdir)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/dbase.db'.format(PWD)
SQLALCHEMY_TRACK_MODIFICATIONS = False

PORT = 8000
DEBUG = True
