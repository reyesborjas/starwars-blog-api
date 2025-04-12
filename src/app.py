import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite, Film

app = Flask(__name__)
app.url_map.strict_slashes = False

# Database configuration - already set up in the Codespaces environment
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

# [GET] /people Get a list of all the people in the database
@app.route('/people', methods=['GET'])
def get_all_people():
    people = Character.query.all()
    all_people = list(map(lambda x: x.serialize(), people))
    return jsonify(all_people), 200

# [GET] /people/<int:people_id> Get one single person information
@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Character.query.get(people_id)
    if person is None:
        raise APIException('Person not found', status_code=404)
    return jsonify(person.serialize()), 200

# [GET] /planets Get a list of all the planets in the database
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))
    return jsonify(all_planets), 200

# [GET] /planets/<int:planet_id> Get one single planet information
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException('Planet not found', status_code=404)
    return jsonify(planet.serialize()), 200

# [GET] /users Get a list of all the blog post users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))
    return jsonify(all_users), 200

# [GET] /users/favorites Get all the favorites that belong to the current user
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    # For demonstration purposes, we'll use a hardcoded user ID
    # In a real application, this would come from authentication
    current_user_id = request.args.get('user_id', 1, type=int)
    
    user = User.query.get(current_user_id)
    if user is None:
        raise APIException('User not found', status_code=404)
    
    favorites = Favorite.query.filter_by(user_id=current_user_id).all()
    all_favorites = list(map(lambda x: x.serialize(), favorites))
    return jsonify(all_favorites), 200

# [POST] /favorite/planet/<int:planet_id> Add a new favorite planet to the current user
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    # For demonstration purposes, we'll use a hardcoded user ID or from request
    request_body = request.get_json(silent=True) or {}
    current_user_id = request_body.get('user_id', 1)
    
    # Check if planet exists
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException('Planet not found', status_code=404)
    
    # Check if user exists
    user = User.query.get(current_user_id)
    if user is None:
        raise APIException('User not found', status_code=404)
    
    # Check if favorite already exists
    existing_favorite = Favorite.query.filter_by(
        user_id=current_user_id, 
        item_type='planet', 
        item_id=planet_id
    ).first()
    
    if existing_favorite:
        return jsonify({"message": "Favorite already exists"}), 400
    
    # Create new favorite
    new_favorite = Favorite(
        user_id=current_user_id,
        item_type='planet',
        item_id=planet_id
    )
    
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite planet added successfully"}), 201

# [POST] /favorite/people/<int:people_id> Add a new favorite character to the current user
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    # For demonstration purposes, we'll use a hardcoded user ID or from request
    request_body = request.get_json(silent=True) or {}
    current_user_id = request_body.get('user_id', 1)
    
    # Check if character exists
    character = Character.query.get(people_id)
    if character is None:
        raise APIException('Character not found', status_code=404)
    
    # Check if user exists
    user = User.query.get(current_user_id)
    if user is None:
        raise APIException('User not found', status_code=404)
    
    # Check if favorite already exists
    existing_favorite = Favorite.query.filter_by(
        user_id=current_user_id, 
        item_type='character', 
        item_id=people_id
    ).first()
    
    if existing_favorite:
        return jsonify({"message": "Favorite already exists"}), 400
    
    # Create new favorite
    new_favorite = Favorite(
        user_id=current_user_id,
        item_type='character',
        item_id=people_id
    )
    
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite character added successfully"}), 201

# [DELETE] /favorite/planet/<int:planet_id> Delete favorite planet
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    # For demonstration purposes, we'll use a hardcoded user ID or from request
    current_user_id = request.args.get('user_id', 1, type=int)
    
    # Find the favorite
    favorite = Favorite.query.filter_by(
        user_id=current_user_id,
        item_type='planet',
        item_id=planet_id
    ).first()
    
    if favorite is None:
        raise APIException('Favorite not found', status_code=404)
    
    # Delete the favorite
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite planet deleted successfully"}), 200

# [DELETE] /favorite/people/<int:people_id> Delete favorite character
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    # For demonstration purposes, we'll use a hardcoded user ID or from request
    current_user_id = request.args.get('user_id', 1, type=int)
    
    # Find the favorite
    favorite = Favorite.query.filter_by(
        user_id=current_user_id,
        item_type='character',
        item_id=people_id
    ).first()
    
    if favorite is None:
        raise APIException('Favorite not found', status_code=404)
    
    # Delete the favorite
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite character deleted successfully"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)