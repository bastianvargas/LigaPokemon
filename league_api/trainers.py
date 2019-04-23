from flask import Blueprint, request, jsonify
from . import db
import json
import random
from league_api.task import crear_trainer
import time
from time import sleep

bp = Blueprint('trainers', __name__, url_prefix='/trainers')


@bp.route('', methods=['GET', 'POST', 'PUT', 'DELETE'])
def trainers_func():
    trainer_id = request.args.get('id')
    request_body = request.get_json()
    if request.method == 'POST':
        result = db.consultar_trainer_por_nombre(request_body['name'])
        if result > 0:
            return "ya existe"

        else:
            lista_pokemons = crear_trainer.delay(request_body)
            while not lista_pokemons.ready():
                sleep(0.5)
            pokemons = lista_pokemons.get()
            request_body['pokemons'] = pokemons
            return jsonify({"_id": db.crear_trainerr(request_body)})

    elif request.method == 'PUT':
        # Actualizar nombre y descripcion de la carrera
        return jsonify({'modificados': db.actualizar_trainer(request_body)})

    elif request.method == 'DELETE' and trainer_id is not None:
        # Borrar una carrera usando el _id
        return jsonify({'borrados': db.borrar_trainer_por_id(trainer_id)})

    elif trainer_id is not None:
        # Obtener trainer por id
        result = db.consultar_trainer_por_id(trainer_id)
        return jsonify({"clase": json.loads(result)})


@bp.route('/porNombre', methods=['POST'])
def trainers_por_nombre():
    request_body = request.get_json()
    result = db.consultar_trainer_por_nombre(request_body["nombre"])
    return jsonify({"trainers": json.loads(result)})


@bp.route('/stats')
def stats_collection():
    return jsonify({"collections": json.loads(db.collection_stats("trainers"))})
