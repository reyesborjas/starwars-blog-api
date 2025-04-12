# In src/app.py
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