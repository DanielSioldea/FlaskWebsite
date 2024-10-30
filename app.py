from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def homePage():
    return render_template('home.html')

@app.route('/shop')
def shopPage():
    items = [
        {'id': 1, 'name': 'Transportinator', 'barcode': 'XHJ123', 'price': 450},
        {'id': 2, 'name': 'Shrinkinator', 'barcode': 'XHJ124', 'price': 720},
        {'id': 3, 'name': 'Reduce-Inator', 'barcode': 'XHJ125', 'price': 75},
        {'id': 4, 'name': 'Shenaniganator', 'barcode': 'XHJ126', 'price': 199},
        {'id': 5, 'name': 'Animate-Inator', 'barcode': 'XHJ127', 'price': 200},
    ]
    return render_template('shop.html', items=items)