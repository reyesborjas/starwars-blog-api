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


db_url = os.getenv("DATABASE_URL", "postgresql://gitpod:postgres@localhost:5432/example")
app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print(f"Using database: {app.config['SQLALCHEMY_DATABASE_URI']}")

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/people', methods=['GET'])
def get_all_people():
    people = Character.query.all()
    all_people = list(map(lambda person: person.serialize(), people))
    
    return jsonify(all_people), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Character.query.get(people_id)
    
    if not person:
        return jsonify({"message": "Person not found"}), 404
        
    return jsonify(person.serialize()), 200


@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    all_planets = list(map(lambda planet: planet.serialize(), planets))
    
    return jsonify(all_planets), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    
    if not planet:
        return jsonify({"message": "Planet not found"}), 404
        
    return jsonify(planet.serialize()), 200


@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    all_users = list(map(lambda user: user.serialize(), users))
    
    return jsonify(all_users), 200


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
  
    user_id = request.args.get('user_id', 1)
    

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
 
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    
  
    result = []
    for fav in favorites:
        item_data = None
        
        if fav.item_type == 'character':
            character = Character.query.get(fav.item_id)
            if character:
                item_data = character.serialize()
        
        elif fav.item_type == 'planet':
            planet = Planet.query.get(fav.item_id)
            if planet:
                item_data = planet.serialize()
        
        if item_data:
            result.append({
                "id": fav.id,
                "type": fav.item_type,
                "item": item_data
            })
    
    return jsonify(result), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_favorite(planet_id):
    # For now, we'll use a hardcoded user ID (in a real app, this would be from authentication)
    user_id = request.json.get('user_id', 1)
    
   
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
   
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"message": "Planet not found"}), 404
    
 
    existing_favorite = Favorite.query.filter_by(
        user_id=user_id, 
        item_type='planet', 
        item_id=planet_id
    ).first()
    
    if existing_favorite:
        return jsonify({"message": "Planet is already in favorites"}), 400
    
  
    new_favorite = Favorite(
        user_id=user_id,
        item_type='planet',
        item_id=planet_id
    )
    
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({"message": "Planet added to favorites successfully"}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_person_favorite(people_id):
 
    user_id = request.json.get('user_id', 1)
    
    # Validate user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
  
    person = Character.query.get(people_id)
    if not person:
        return jsonify({"message": "Person not found"}), 404
    
   
    existing_favorite = Favorite.query.filter_by(
        user_id=user_id, 
        item_type='character', 
        item_id=people_id
    ).first()
    
    if existing_favorite:
        return jsonify({"message": "Person is already in favorites"}), 400
    
    
    new_favorite = Favorite(
        user_id=user_id,
        item_type='character',
        item_id=people_id
    )
    
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({"message": "Person added to favorites successfully"}), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(planet_id):
    
    user_id = request.args.get('user_id', 1)
    
   
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    
    favorite = Favorite.query.filter_by(
        user_id=user_id, 
        item_type='planet', 
        item_id=planet_id
    ).first()
    
    if not favorite:
        return jsonify({"message": "Planet favorite not found"}), 404
    
   
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"message": "Planet removed from favorites successfully"}), 200


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_person_favorite(people_id):
    # For now, we'll use a hardcoded user ID (in a real app, this would be from authentication)
    user_id = request.args.get('user_id', 1)
    
   
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
   
    favorite = Favorite.query.filter_by(
        user_id=user_id, 
        item_type='character', 
        item_id=people_id
    ).first()
    
    if not favorite:
        return jsonify({"message": "Person favorite not found"}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"message": "Person removed from favorites successfully"}), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)