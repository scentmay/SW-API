"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# get all people
@app.route('/allpeople', methods=['GET'])
def getAllPeople():
    try:
        people = People.query.all()
        people_serialize = list(map(lambda x: x.serialize(), people))
        return jsonify(people_serialize)
    except:
        raise APIException('No hay personajes en la BBDD', 404)


# get one people
@app.route('/allpeople/<int:people_id>')
def getOnePeople(people_id):
    try:
        people = People.query.get(people_id)
        return jsonify(people.serialize())
    except:
        raise APIException('Personaje no encontrado', 404)


# get all planets
@app.route('/allplanets', methods=['GET'])
def getAllPlanets():
    try:
        planet = Planet.query.all()
        planet_serialize = list(map(lambda x: x.serialize(), planet))
        return jsonify(planet_serialize)
    except:
        raise APIException('No hay planetas en la BBDD', 404)

# get one planet
@app.route('/allplanets/<int:planet_id>')
def getOnePlanet():
    try:
        planet = Planet.query.get(planet_id)
        return jsonify(planet.serialize())
    except:
        raise APIException('Planeta no encontrado', 404)

# get all users
@app.route('/allusers', methods=['GET'])
def getAllUsers():
    try:
        users = User.query.all()
        users_serialize = list(map(lambda x: x.serialize(), users))
        return jsonify(people_serialize)
    except:
        raise APIException('No hay usuarios en la BBDD', 404)


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
