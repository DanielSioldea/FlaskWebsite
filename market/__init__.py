import os
import config
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Define the instance path inside the 'market' folder
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')

# Ensure the instance folder exists
os.makedirs(instance_path, exist_ok=True)

app = Flask(__name__, instance_path=instance_path)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "shop.db")}'
app.config['SECRET_KEY'] = config.secret_key
db = SQLAlchemy(app)
bcrypt = Bcrypt(app) 

from market import routes
from market.models import Item

with app.app_context():
    db.create_all()

