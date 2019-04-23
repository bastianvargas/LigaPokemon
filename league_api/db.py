from bson.json_util import dumps, ObjectId
from flask import current_app
from pymongo import MongoClient, DESCENDING
from werkzeug.local import LocalProxy




# Este método se encarga de configurar la conexión con la base de datos
def get_db():
    liga_db = current_app.config['DB_URI']
    client = MongoClient(liga_db)
    return client.liga_pokemon

# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


def test_connection():
    return dumps(db.collection_names())


def collection_stats(collection_name):
    return dumps(db.command('collstats', collection_name))



#--------

def crear_league(json):
    return str(db.leagues.insert_one(json).inserted_id)


def consultar_league_por_id(league_id):
    return dumps(db.leagues.find_one({'_id': ObjectId(league_id)}))


def actualizar_league(league):
    # Esta funcion solamente actualiza nombre y descripcion de la league
    return str(db.leagues.update_one({'_id': ObjectId(league['_id'])},
                           {'$set': {'name': league['name'], 'trainer': league['descripcion']}})
               .modified_count)



# Clase de operadores
def consultar_leagues(skip, limit):
    return dumps(db.leagues.find({}).skip(int(skip)).limit(int(limit)))

# AGREGAR ENTRENADOR
def add_trainer(json):
    trainer = consultar_trainer_por_id_proyeccion(json['id_trainer'], proyeccion={'name': 1})
    trainer['score'] = 0
    print("esto tiene trainer: ", trainer)
    return str(db.leagues.update_one({'_id': ObjectId(json['id_league'])}, {'$addToSet': {'position_table': trainer}}).modified_count)


#trainers-------

def crear_trainerr(json):
    print("hola", json)
    return str(db.trainers.insert_one(json).inserted_id)


def consultar_trainer_por_id(id_trainer):
    return dumps(db.trainers.find_one({'_id': ObjectId(id_trainer)}))

def consultar_trainer_retador1_por_id(id_trainer):
    return db.trainers.find_one({'_id': ObjectId(id_trainer.get('challenger_1'))})

def consultar_trainer_retador2_por_id(id_trainer):
    return db.trainers.find_one({'_id': ObjectId(id_trainer.get('challenger_2'))})

def consultar_trainer_por_nombre(name_trainer):
    return db.trainers.count_documents({"name": name_trainer})


def actualizar_trainer(trainer):
    # Esta funcion solamente actualiza nombre, descripcion y clases del trainer
    return str(db.trainers.update_one({'_id': ObjectId(trainer['_id'])},  {'$set': {'nombre': trainer['nombre']}}).modified_count)





def consultar_trainer_por_id_proyeccion(id_trainer, proyeccion=None):
    return db.trainers.find_one({'_id': ObjectId(id_trainer)}, proyeccion)
