from market import app
from flask import render_template, redirect, url_for, flash
from market.models import Item, User
from market.forms import RegisterForm, LoginForm
from market import db
from flask_login import login_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def homePage():
    return render_template('home.html')


@app.route('/shop')
@login_required
def shopPage():
    items = Item.query.all()
    print(items)
    return render_template('shop.html', items=items)


@app.route('/villanyCourse')
@login_required
def villanyCourse():
    return render_template('villanyCourse.html')

@app.route('/register', methods=['GET', 'POST'])
def registerPage():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, 
                              email_address=form.email_address.data, 
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Welcome aboard {user_to_create.username}! Need to put together a scheme? <a href="{url_for("villanyCourse")}" class="alert-link"> Click here</a> to sign up for our Villany course!', category='success')

        return redirect(url_for('shopPage'))
    
    if form.errors != {}: # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/termsConditions')
def termsPage():
    return render_template('termsCond.html')

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Welcom back {attempted_user.username}! Browse some gizmos for some neerdowelling', category='success')
            return redirect(url_for('shopPage'))
        else:
            flash('Invalid credentials! Please try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logoutPage():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('homePage'))