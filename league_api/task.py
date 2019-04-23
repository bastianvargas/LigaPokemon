from celery import Celery, task
import random
from flask import jsonify, Flask
from league_api.flask_celery import make_celery
import requests
import os

rabbitmq_user = os.environ['RABBITMQ_USER']
rabbitmq_pass = os.environ['RABBITMQ_PASS']
rabbitmq_host = os.environ['RABBITMQ_HOST']
rabbitmq_vhost = os.environ['RABBITMQ_VHOST']
rabbitmq_port = os.environ['RABBITMQ_PORT']
mongodb_host = os.environ['MONGODB_HOST']
mongodb_port = os.environ['MONGODB_PORT']
mongodb_db = os.environ['MONGODB_DATABASE']

BROKER_URL = 'mongodb://{}:{}/{}'.format(mongodb_host, mongodb_port, mongodb_db)
app = Celery('tasks', broker='amqp://{}:{}@{}:{}/{}'.format(rabbitmq_user, rabbitmq_pass, rabbitmq_host, rabbitmq_port, rabbitmq_vhost), backend=BROKER_URL)

app= Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://{}:{}@{}:{}/{}'.format(rabbitmq_user, rabbitmq_pass, rabbitmq_host, rabbitmq_port, rabbitmq_vhost)
app.config['CELERY_RESULT_BACKEND'] = 'mongodb://{}:{}/{}'.format(mongodb_host, mongodb_port, mongodb_db)
celery = make_celery(app)

@app.route('/process/<name>')
def process(name):
    return name


@celery.task(name='task.crear_trainer')
def crear_trainer(json):
    num_pokemons = json['pokemons']
    randoms_pokemons = []
    list_pokemon = []
    for i in range(num_pokemons):
        id_poke = random.randrange(964)
        randoms_pokemons.append(id_poke)
        pokemon=get_pokemon(id_poke)
        list_pokemon.append(pokemon)
    return list_pokemon

def get_pokemon(id):
    url = 'http://pokeapi.co/api/v2/pokemon/{}/'.format(id)
    response = requests.get(url)
    payload = response.json()
    pokemon = {'name': payload['name'],
            'speed': payload['stats'][0].get('base_stat'),
            'attk': payload['stats'][4].get('base_stat'),
            'hp': payload['stats'][5].get('base_stat')}
    return pokemon



if __name__ == '__main__':
    app.run(debug=True)
