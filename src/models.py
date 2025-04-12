from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Text, Boolean, Table
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()

# Association tables for many-to-many relationships
character_films = db.Table('character_films',
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'), primary_key=True),
    db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True)
)

planet_films = db.Table('planet_films',
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id'), primary_key=True),
    db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    is_active = db.Column(db.Boolean(), nullable=False, default=True)
    
    favorites = db.relationship("Favorite", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_type = db.Column(db.String(50), nullable=False)  # 'character' or 'planet'
    item_id = db.Column(db.Integer, nullable=False)
    
    user = db.relationship("User", back_populates="favorites")

    def __repr__(self):
        return f"<Favorite {self.item_type}:{self.item_id} by User {self.user_id}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "item_type": self.item_type,
            "item_id": self.item_id
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    height = db.Column(db.Float, nullable=True)
    mass = db.Column(db.Float, nullable=True)
    hair_color = db.Column(db.String(50), nullable=True)
    skin_color = db.Column(db.String(50), nullable=True)
    eye_color = db.Column(db.String(50), nullable=True)
    birth_year = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    
    homeworld_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    homeworld = db.relationship("Planet", back_populates="residents")
    
    films = db.relationship("Film", secondary=character_films, back_populates="characters")

    def __repr__(self):
        return f'<Character {self.name}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "description": self.description,
            "homeworld_id": self.homeworld_id
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rotation_period = db.Column(db.Integer, nullable=True)
    orbital_period = db.Column(db.Integer, nullable=True)
    diameter = db.Column(db.Integer, nullable=True)
    climate = db.Column(db.String(100), nullable=True)
    gravity = db.Column(db.String(100), nullable=True)
    terrain = db.Column(db.String(100), nullable=True)
    surface_water = db.Column(db.Float, nullable=True)
    population = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    
    residents = db.relationship("Character", back_populates="homeworld")
    films = db.relationship("Film", secondary=planet_films, back_populates="planets")

    def __repr__(self):
        return f'<Planet {self.name}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population": self.population,
            "description": self.description
        }

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    episode_id = db.Column(db.Integer, nullable=True)
    opening_crawl = db.Column(db.Text, nullable=True)
    director = db.Column(db.String(100), nullable=True)
    producer = db.Column(db.String(100), nullable=True)
    release_date = db.Column(db.DateTime, nullable=True)
    
    characters = db.relationship("Character", secondary=character_films, back_populates="films")
    planets = db.relationship("Planet", secondary=planet_films, back_populates="planets")

    def __repr__(self):
        return f'<Film {self.title}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "episode_id": self.episode_id,
            "opening_crawl": self.opening_crawl,
            "director": self.director,
            "producer": self.producer,
            "release_date": self.release_date.strftime("%Y-%m-%d") if self.release_date else None
        }