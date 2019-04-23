from flask import Blueprint, request, jsonify
from . import db
import json
from bson.json_util import ObjectId

bp = Blueprint('leagues', __name__, url_prefix='/leagues')


@bp.route('', methods=['GET', 'POST', 'PUT', 'DELETE'])
def leagues_func():
    league_id = request.args.get('id')


    request_body = request.get_json()
    if request.method == 'POST':
        # Crear league
        return jsonify({'_id': db.crear_league(request_body)})
    elif request.method == 'PUT':
        # Actualizar nombre y descripcion de la league
        return jsonify({'modificados': db.actualizar_league(request_body)})
    elif request.method == 'DELETE' and league_id is not None:
        # Borrar una league usando el _id
        return jsonify({'borrados': db.borrar_league_por_id(league_id)})
    elif league_id is not None:
        # Obtener leagues por _id
        result = db.consultar_league_por_id(league_id)
        return jsonify({'league': json.loads(result)})
    else:
        # Obtener leagues

        result = db.consultar_leagues()
        return jsonify({'leagues': json.loads(result)})






#agregar entrenador ++++++++

@bp.route('/add-trainer', methods=['PUT'])
def add_trainer():
    request_body = request.get_json()
    if request.method == 'PUT':
        return jsonify({'modificados': json.loads(db.add_trainer(request_body))})

@bp.route('/official-battle', methods=['PUT'])
def official_battle():
    request_body = request.get_json()
    league_id = request.args.get('id')
    if request.method == 'PUT':
        challenger_1 = db.consultar_trainer_retador1_por_id(request_body)
        challenger_2 = db.consultar_trainer_retador2_por_id(request_body)
        print(type(challenger_1))
        print("tipo1: ", challenger_1)
        print("tipo1.2: ", challenger_1)
        print("tipo2: ", challenger_2)
        suma1 = 0
        suma2 = 0
        win = ''
        for c in challenger_1.get('pokemons'):
            suma1 += c['speed']
            print(suma1)

        for c in challenger_2.get('pokemons'):
            suma2 += c['speed']
            print(suma2)
        if suma1 != suma2 and suma1 > suma2:
            win = challenger_1.get('_id')
        elif suma1 != suma2 and suma2 > suma1:
            win = challenger_2.get('_id')
        print(win)

        return win
        # return jsonify({'modificados': json.loads(db.actualizar_league(request_body))})



@bp.route('/test')
def test_connection():
    return jsonify({'collections': json.loads(db.test_connection())})
