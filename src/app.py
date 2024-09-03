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
from models import db, User, Planets, People, Vehicles, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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

@app.route('/people', methods=['GET'])
def obtener_personas():
    try:
        people_list = []
        people = People.query.all()

        if people == []:
            return jsonify({"Error": "No se ha encontrado"}), 404
        
        for person in people:
            people_list.append(person.serialize())

        return jsonify(people_list), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/people/<int:people_id>', methods=['GET'])
def obtener_persona_id(people_id):
    try:
        people = People.query.get(people_id)

        if not people:
            return jsonify({"Error": "No se ha encontrado"}), 404
        
        return jsonify(people.serialize()), 200
        
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/planets', methods=['GET'])
def obtener_planetas():
    try:
        planets_list = []
        planets = Planets.query.all()

        if not planets:
            return jsonify({"Error": "No se ha encontrado"}), 404
        
        for planet in planets:
            planets_list.append(planet.serialize())
        
        return jsonify(planets_list)

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/vehicles', methods=['GET'])
def obtener_vehiculos():
    try:
        vehicles_list = []

        vehicles = Vehicles.query.all()

        if not vehicles:
            return jsonify({"Error": "No se ha encontrado ningún vehiculo"}), 404
        
        for vehicle in vehicles:
            vehicles_list.append(vehicle.serialize())
        
        return jsonify(vehicles_list), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route('/planets/<int:planet_id>', methods=['GET'])
def obtener_planeta_id(planet_id):
    try:
        planet = Planets.query.get(planet_id)

        if not planet:
            return jsonify({"Error": "No se ha encontrado"}), 404
        
        return jsonify(planet.serialize())
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
    
@app.route('/users', methods=['GET'])
def obtener_usuario():
    try:
        user_list = []
        users = User.query.all()

        if users == []:
            return jsonify({"Error": "No se ha encontrado"}), 404
        
        for user in users:
            user_list.append(user.serialize())

        return jsonify(user_list),200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/users/favorites', methods=['GET'])
def obtener_favoritos():
    try:
        user = User.query.get(2)
        favoritos = [favorito.serialize() for favorito in user.favoritos]

        return jsonify({"Favoritos": favoritos}), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def agregar_fav_planeta(planet_id):
    try:
        data = request.get_json()
        user_id = data.get("user_id")

        planeta = Planets.query.get(planet_id)
        if planeta is None:
            return jsonify({"Error": "El planeta no existe"}), 404

        if not user_id:
            return jsonify({"Error": "No se ha encontrado usuario"}), 404
        
        
        planeta_favorito = Favorite(user_id = user_id, planet_id = planet_id) 

        db.session.add(planeta_favorito)
        db.session.commit()

        return jsonify({"message": "Planeta favorito añadido con éxito"}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}, 500)
    
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def agregar_fav_people(people_id):
    try:
        data = request.get_json()
        user_id = data.get("user_id")

        person = People.query.get(people_id)
        if person is None:
            return jsonify({"Error": "La persona no existe"}), 404
        
        if not user_id:
            return jsonify({"Error": "No se ha encontrado usuario"}), 404
        
        persona_favorita = Favorite(user_id = user_id, people_id = people_id)

        db.session.add(persona_favorita)
        db.session.commit()

        return jsonify({"message": "Persona favorita añadida con exito"})

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def eliminar_fav_planeta(planet_id):
    try:
        data = request.get_json()
        user_id = data.get("user_id")

        favorito = Favorite.query.filter_by(user_id = user_id, planet_id = planet_id).first()

        if favorito is None:
            return jsonify({"Error": "No se ha encontrado favorito"}), 404
        
        db.session.delete(favorito)
        db.session.commit()

        return jsonify({"message": "Favorito eliminado"}), 200


    except Exception as e: 
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def eliminar_fav_people(people_id):
    try:
        data = request.get_json()
        user_id = data.get("user_id")

        favorito = Favorite.query.filter_by(user_id = user_id, people_id = people_id).first()

        if favorito is None:
            return jsonify({"Error": "No se ha encontrado favorito"}), 404
        
        db.session.delete(favorito)
        db.session.commit()

        return jsonify({"message": "Favorito eliminado"}), 200


    except Exception as e: 
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/planet', methods=['POST'])
def agregar_planeta():
    try:
        data = request.get_json()

        name = data.get("name")
        gravity = data.get("gravity")
        population = data.get("population")
        terrain = data.get("terrain")

        if not name or not gravity or not population or not terrain:
            return jsonify({"error": "name, gravity, population and terrain are required"}), 400

        existing_planet = Planets.query.filter_by(name=name).first()
        if existing_planet:
            return jsonify({"Error": "El planeta ya existe"}), 400
        
        new_planet = Planets(name=name, gravity=gravity, population=population, terrain=terrain)

        db.session.add(new_planet)
        db.session.commit()

        return jsonify({"message": "Planet created successfully", "Planet": new_planet.serialize()})


    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route('/planet/<int:planet_id>', methods=['PUT'])
def editar_planeta(planet_id):
    try:

        planeta = Planets.query.get(planet_id)
        if not planeta:
            return jsonify({"error": "Planeta no encontrado"}), 404

        data = request.get_json()
        name = data.get("name")
        gravity = data.get("gravity")
        population = data.get("population")
        terrain = data.get("terrain")

        if not name or not gravity or not population or not terrain:
            return jsonify({"error": "name, gravity, population and terrain are required"}), 400

        existing_planet = Planets.query.filter(Planets.name == name, Planets.id != planet_id).first()
        if existing_planet:
            return jsonify({"Error": "El planeta ya existe"}), 400

        planeta.name = name
        planeta.gravity = gravity
        planeta.population = population
        planeta.terrain = terrain

        db.session.commit()

        new_planeta = {
            "id": planeta.id,
            "name": planeta.name,
            "gravity": planeta.gravity,
            "population": planeta.population,
            "terrain": planeta.terrain
        }

        return jsonify({"message": "Planeta actualizado", "Planeta actualizado": new_planeta}), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/planet/<int:planeta_id>', methods=['DELETE'])
def eliminar_planeta(planeta_id):
    try:
        planeta = Planets.query.get(planeta_id)
        if not planeta:
            return jsonify({"error": "Planeta no encontrado"}), 404
        
        db.session.delete(planeta)
        db.session.commit()

        return jsonify({"message": "Planet deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500



@app.route('/people/', methods=['POST'])
def agregar_persona():
    try:
        data = request.get_json()

        name = data.get("name")
        gender = data.get("gender")
        birth_year = data.get("birth_year")
        mass = data.get("mass")

        if not name or not gender or not birth_year or not mass:
            return jsonify({"error": "Name, gender and birth_year are required"}), 400
        
        existing_people = People.query.filter_by(name = name).first()
        if existing_people:
            return jsonify({"error": "La persona ya existe"}), 400

        new_person = People(name = name, gender = gender, birth_year = birth_year, mass = mass)

        db.session.add(new_person)
        db.session.commit()

        return jsonify({"message": "Person created successfully", "People": new_person.serialize()}), 200

    except Exception as e: 
        return jsonify({"error": "Internal server error", "message": str(e)}),500
    
@app.route('/people/<int:person_id>', methods=['PUT'])
def editar_persona(person_id):
    try:
        persona = People.query.get(person_id)
        if not persona:
            return jsonify({"error": "Persona no encontrada"}), 404

        data = request.get_json()
        name = data.get("name")
        gender = data.get("gender")
        birth_year = data.get("birth_year")
        mass = data.get("mass")

        if not name or not gender or not birth_year or not mass:
            return jsonify({"error": "name, gender, birth_year y mass son requeridos"}), 400

        existing_person = People.query.filter(People.name == name, People.id != person_id).first()
        if existing_person:
            return jsonify({"Error": "La persona ya existe"}), 400

        persona.name = name
        persona.gender = gender
        persona.birth_year = birth_year
        persona.mass = mass

        db.session.commit()

        updated_persona = {
            "id": persona.id,
            "name": persona.name,
            "gender": persona.gender,
            "birth_year": persona.birth_year,
            "mass": persona.mass
        }

        return jsonify({"message": "Persona actualizada", "Persona actualizada": updated_persona}), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/people/<int:person_id>', methods=['DELETE'])
def eliminar_persona(person_id):
    try:

        persona = People.query.get(person_id)
        if not persona:
            return jsonify({"error": "Persona no encontrada"}), 404

        db.session.delete(persona)
        db.session.commit()

        return jsonify({"message": "Persona eliminada con éxito"}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/vehicle', methods=['POST'])
def agregar_vehiculo():
    try:
        data = request.get_json()

        name = data.get("name")
        model = data.get("model")
        manufacturer = data.get("manufacturer")
        cost_in_credits = data.get("cost_in_credits")

        if not name or not model or not manufacturer or not cost_in_credits:
            return jsonify({"error": "Name, model, manufacturer, and cost_in_credits are required"}), 400

        existing_vehicle = Vehicles.query.filter_by(name=name).first()
        if existing_vehicle:
            return jsonify({"error": "El vehiculo ya existe"}), 400

        new_vehicle = Vehicles(
            name = name,
            model = model,
            manufacturer = manufacturer,
            cost_in_credits = cost_in_credits
        )

        db.session.add(new_vehicle)
        db.session.commit()

        return jsonify({"message": "Vehiculo creado con exito", "Vehicle": new_vehicle.serialize()}), 201

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def editar_vehiculo(vehicle_id):
    try:
        
        vehiculo = Vehicles.query.get(vehicle_id)
        if not vehiculo:
            return jsonify({"error": "Vehiculo no encontrado"}), 404

        
        data = request.get_json()
        name = data.get("name")
        model = data.get("model")
        manufacturer = data.get("manufacturer")
        cost_in_credits = data.get("cost_in_credits")

        
        if not name or not model or not manufacturer or not cost_in_credits:
            return jsonify({"error": "name, model, manufacturer y cost_in_credits son requeridos"}), 400

        
        existing_vehicle = Vehicles.query.filter(Vehicles.name == name, Vehicles.id != vehicle_id).first()
        if existing_vehicle:
            return jsonify({"Error": "El vehiculo ya existe"}), 400

        
        vehiculo.name = name
        vehiculo.model = model
        vehiculo.manufacturer = manufacturer
        vehiculo.cost_in_credits = cost_in_credits

        db.session.commit()

        updated_vehiculo = {
            "id": vehiculo.id,
            "name": vehiculo.name,
            "model": vehiculo.model,
            "manufacturer": vehiculo.manufacturer,
            "cost_in_credits": vehiculo.cost_in_credits
        }

        return jsonify({"message": "Vehiculo actualizado", "Vehiculo actualizado": updated_vehiculo}), 200

    except Exception as e:

        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def eliminar_vehiculo(vehicle_id):
    try:

        vehiculo = Vehicles.query.get(vehicle_id)
        if not vehiculo:
            return jsonify({"error": "Vehiculo no encontrado"}), 404


        db.session.delete(vehiculo)
        db.session.commit()

        return jsonify({"message": "Vehiculo eliminado con exito"}), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
