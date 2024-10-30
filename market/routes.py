from market import app
from flask import render_template
from market.models import Item, User

@app.route('/')
@app.route('/home')
def homePage():
    return render_template('home.html')

@app.route('/shop')
def shopPage():
    items = Item.query.all()
    print(items)
    return render_template('shop.html', items=items)