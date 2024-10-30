from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    barcode = db.Column(db.String(12), nullable=False, unique=True)

    def __repr__(self):
        return f'Item {self.name}'

@app.route('/')
@app.route('/home')
def homePage():
    return render_template('home.html')

@app.route('/shop')
def shopPage():
    items = Item.query.all()
    # items = [
    #     {'id': 1, 'name': 'Transportinator', 'description': 'Instantly transport an object anywhere you can see', 'price': 450},
    #     {'id': 2, 'name': 'Shrinkinator', 'description': 'Self explanatory', 'price': 720},
    #     {'id': 3, 'name': 'Reduce-Inator', 'description': 'Like the Shrinkinator but has a 95% chance to explode', 'price': 75},
    #     {'id': 4, 'name': 'Shenaniganator', 'description': 'Anyone hit by its blast becomes a scoundrel', 'price': 199},
    #     {'id': 5, 'name': 'Chicken Replace-Inator', 'description': 'Swaps anything it hits with the closest chicken in proximity', 'price': 200},
    # ]
    return render_template('shop.html', items=items)

with app.app_context():
    db.create_all()