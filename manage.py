from flask_script import Manager
from aplication.app import app, db
from aplication.models import *

manager = Manager(app)
app.config['DEBUG'] = True

@manager.command
def create_table():
    db.create_all()

@manager.command
def drop_tables():
    db.drop_all()










if __name__ == '__main__':
    manager.run()
