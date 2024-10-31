from market import app
from flask import render_template, redirect, url_for
from market.models import Item, User
from market.forms import RegisterForm
from market import db

@app.route('/')
@app.route('/home')
def homePage():
    return render_template('home.html')

@app.route('/shop')
def shopPage():
    items = Item.query.all()
    print(items)
    return render_template('shop.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def registerPage():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, 
                              email_address=form.email_address.data, 
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('shopPage'))
    
    if form.errors != {}: # If there are not errors from the validations
        for err_msg in form.errors.values():
            print(f'{err_msg}')

    return render_template('register.html', form=form)