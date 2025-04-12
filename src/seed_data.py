from app import app, db
from models import User, Character, Planet, Favorite, Film
from datetime import datetime

def seed_database():
    with app.app_context():
        db.create_all()
        Favorite.query.delete()
        Character.query.delete()
        Planet.query.delete()
        Film.query.delete()
        User.query.delete()
        
        print("Creating test users...")
        
        luke = User(
            username="luke_skywalker",
            email="luke@rebellion.org",
            password="usetheforce",
            first_name="Luke",
            last_name="Skywalker",
            is_active=True
        )
        
        leia = User(
            username="princess_leia",
            email="leia@rebellion.org",
            password="alderaan",
            first_name="Leia",
            last_name="Organa",
            is_active=True
        )
        
        print("Creating planets...")
        
        tatooine = Planet(
            name="Tatooine",
            rotation_period=23,
            orbital_period=304,
            diameter=10465,
            climate="arid",
            gravity="1 standard",
            terrain="desert",
            surface_water=1.0,
            population="200000",
            description="A harsh desert world orbiting twin suns"
        )
        
        alderaan = Planet(
            name="Alderaan",
            rotation_period=24,
            orbital_period=364,
            diameter=12500,
            climate="temperate",
            gravity="1 standard",
            terrain="grasslands, mountains",
            surface_water=40.0,
            population="2000000000",
            description="A peaceful world known for its beauty and democracy"
        )
        
        print("Creating characters...")
       
        luke_character = Character(
            name="Luke Skywalker",
            height=172.0,
            mass=77.0,
            hair_color="blond",
            skin_color="fair",
            eye_color="blue",
            birth_year="19BBY",
            gender="male",
            description="Farm boy turned Jedi Knight"
        )
        
        leia_character = Character(
            name="Leia Organa",
            height=150.0,
            mass=49.0,
            hair_color="brown",
            skin_color="light",
            eye_color="brown",
            birth_year="19BBY",
            gender="female",
            description="Princess of Alderaan and Rebellion leader"
        )
        
        vader = Character(
            name="Darth Vader",
            height=202.0,
            mass=136.0,
            hair_color="none",
            skin_color="white",
            eye_color="yellow",
            birth_year="41.9BBY",
            gender="male",
            description="Dark Lord of the Sith"
        )
        
        print("Creating film...")
        
        a_new_hope = Film(
            title="A New Hope",
            episode_id=4,
            opening_crawl="It is a period of civil war...",
            director="George Lucas",
            producer="Gary Kurtz, Rick McCallum",
            release_date=datetime(1977, 5, 25)
        )
        
        
        db.session.add(luke)
        db.session.add(leia)
        db.session.add(tatooine)
        db.session.add(alderaan)
        db.session.add(luke_character)
        db.session.add(leia_character)
        db.session.add(vader)
        db.session.add(a_new_hope)
        
       
        db.session.commit()
        
        print("Setting up relationships...")
       
        luke_character.homeworld = tatooine
        leia_character.homeworld = alderaan
        
       
        a_new_hope.characters.append(luke_character)
        a_new_hope.characters.append(leia_character)
        a_new_hope.characters.append(vader)
        a_new_hope.planets.append(tatooine)
        a_new_hope.planets.append(alderaan)
        
        print("Creating favorites...")
        # Create some favorites
        luke_fav_vader = Favorite(
            user_id=luke.id,
            item_type='character',
            item_id=vader.id
        )
        
        luke_fav_tatooine = Favorite(
            user_id=luke.id,
            item_type='planet',
            item_id=tatooine.id
        )
        
        leia_fav_alderaan = Favorite(
            user_id=leia.id,
            item_type='planet',
            item_id=alderaan.id
        )
        
        db.session.add(luke_fav_vader)
        db.session.add(luke_fav_tatooine)
        db.session.add(leia_fav_alderaan)
        
       
        db.session.commit()
        
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()