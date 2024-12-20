import sys
sys.path.append('chatbot_ai')
from market import app
from flask import render_template, redirect, url_for, flash, request, session, jsonify
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, AddToCart, ReturnItemForm, CheckoutForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user
from chatbot_ai.chat import get_response

@app.route('/')
@app.route('/home')
def homePage():
    return render_template('home.html')

@app.route('/shop', methods=['GET', 'POST'])
@login_required
def shopPage():

    if 'cart_item' not in session:
        session['cart_item'] = []

    add_to_cart_form = AddToCart()
    return_form = ReturnItemForm()
    if request.method == 'POST':
        # Add to cart logic
        cart_item = request.form.get('cart_item')
        item_to_add = Item.query.filter_by(name=cart_item).first()

        if item_to_add:
            if current_user.can_purchase(item_to_add):
                flash(f'{item_to_add.name} added to your cart!', category='success')
                session['cart_item'].append(item_to_add.name)
                session.modified = True
            else:
                flash(f"Unfortunately, you don't have enough funds to purchase the {item_to_add.name}!", category='danger')

        # Return/remove from cart logic
        item_to_remove = request.form.get('returned_item')
        item_to_return = Item.query.filter_by(name=item_to_remove).first()

        if item_to_return:
            if current_user.can_sell(item_to_return):
                flash(f'{item_to_return.name} has been returned and you have been refunded ${ item_to_return.price // 2 }!', category='info')
                item_to_return.sell(current_user)
                if item_to_return.name in session['cart_item']:
                    session['cart_item'].remove(item_to_return.name)
                    session.modified = True
            else:
                flash(f"You can't return an item you don't own! You might be more evil than I thought!", category='danger')

        return redirect(url_for('shopPage'))
    
    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_item = Item.query.filter_by(owner=current_user.id)
        in_cart = Item.query.filter(Item.name.in_(session['cart_item']))
        return render_template('shop.html', items=items, add_to_cart_form=add_to_cart_form, in_cart=in_cart, owned_item=owned_item, return_form=return_form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profilePage():
    add_to_cart_form = AddToCart()
    return_form = ReturnItemForm()
    owned_item = Item.query.filter_by(owner=current_user.id).all()

    # Return/remove from cart logic
    item_to_remove = request.form.get('returned_item')
    item_to_return = Item.query.filter_by(name=item_to_remove).first()

    if request.method == 'POST':
        if item_to_return:
            if current_user.can_sell(item_to_return):
                flash(f'{item_to_return.name} has been returned and you have been refunded ${ item_to_return.price // 2 }!', category='info')
                item_to_return.sell(current_user)
                db.session.commit()
            else:
                flash(f"You can't return an item you don't own! You might be more evil than I thought!", category='danger')
        return redirect(url_for('profilePage'))

    return render_template('profile.html', owned_item=owned_item, add_to_cart_form=add_to_cart_form, return_form=return_form)

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkoutPage():
    checkout_form = CheckoutForm(
        first_name=current_user.billing_first_name,
        last_name=current_user.billing_last_name,
        email=current_user.email_address,
        address=current_user.billing_address,
        address2=current_user.billing_address2,
        city=current_user.billing_city,
        zip_code=current_user.billing_zip_code
    )
    
    # Check if 'cart_item' exists in session
    if 'cart_item' in session:
        cart_items = Item.query.filter(Item.name.in_(session['cart_item'])).all()
    else:
        cart_items = []

    if request.method == 'POST' and checkout_form.validate_on_submit():
        for item in cart_items:
            item.owner = current_user.id
        db.session.commit()
        item.buy(current_user)

        
            # Save billing information for next time
        if checkout_form.save_info.data:
            current_user.billing_first_name = checkout_form.first_name.data
            current_user.billing_last_name = checkout_form.last_name.data
            current_user.billing_address = checkout_form.address.data
            current_user.billing_address2 = checkout_form.address2.data
            current_user.billing_city = checkout_form.city.data
            current_user.billing_zip_code = checkout_form.zip_code.data
            db.session.commit()

        session.pop('cart_item', None)
        flash('Thank you for shopping with us! Your items will be shipped to you in 3-5 business days!', category='success')
        return redirect(url_for('profilePage'))
    else:
        # Print form errors to the console
        print(checkout_form.errors)
        # Flash form errors to the user
        for field, errors in checkout_form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(checkout_form, field).label.text}: {error}", category='danger')
    
    add_to_cart_form = AddToCart()
    total_price = sum(item.price for item in cart_items)
    cart_count = len(cart_items)

    return render_template('checkout.html', cart_items=cart_items, add_to_cart_form=add_to_cart_form, total_price=total_price, cart_count=cart_count, checkout_form=checkout_form)

    

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
    

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", category='danger')

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
            flash(f'Welcome back {attempted_user.username}! Browse some gizmos for some neerdowelling', category='success')
            return redirect(url_for('shopPage'))
        else:
            flash('Invalid credentials! Please try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logoutPage():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('homePage'))

@app.route('/predict', methods=['POST'])    
def predict():
    text = request.get_json().get("message")

    # if text == 'hello':
    #     response = 'Welcome to Doofenshmirtz Evil Inc. What scheeming do you need help with today?'
    # else:
    #     response = 'I am not programmed to respond to that'

    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)