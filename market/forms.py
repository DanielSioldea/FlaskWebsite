from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User
import re

def password_check(form, field):
    password = field.data
    if len(password) >= 6:
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        elif not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        elif not re.search(r'[0-9]', password):
            raise ValidationError('Password must contain at least one digit.')
        elif not re.search(r'[^a-zA-Z0-9]', password):
            raise ValidationError('Password must contain at least one special character.')


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username.')
        
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address.')

    username = StringField(label='User Name', validators=[Length(min=3, max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired(), password_check])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Submit')

class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Enter')

class AddToCart(FlaskForm):
    submit = SubmitField(label='Add to Cart')

class CheckoutForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    address = StringField('Address', validators=[DataRequired()])
    address2 = StringField('Address 2')
    city = StringField('City', validators=[DataRequired()])
    zip_code = StringField('Zip code', validators=[DataRequired()])
    save_info = BooleanField('Save this information for next time')
    submit = SubmitField(label='Checkout')

class ReturnItemForm(FlaskForm):
    submit = SubmitField(label="Return 'Inator")