from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from aplication import config
import os




app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

from aplication.models import League, Trainer, Position_Table, Pokemon

@app.route('/', methods=['GET'])
def index():
    return "index"
