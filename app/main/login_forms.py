
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

def password_strength_ok(password):
    if len(password) < 8:
        return False
    
    has_upper = False
    has_lower = False
    has_digit = False
    has_other = False

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        else:
            has_other = True    
    return has_upper and has_lower and has_digit and has_other     
    


#Forms for login and registration
class LoginForm(FlaskForm):
    username = StringField('Username/Email', validators=[DataRequired()], render_kw={"placeholder": "Enter Username/Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    registration_code = StringField('Registration Code', validators=[DataRequired()], render_kw={"placeholder": "Enter Registration Code"})
    username = StringField('Username/Login', validators=[DataRequired()], render_kw={"placeholder": "Enter Username"})
    display_name = StringField('Full Name', validators=[DataRequired()], render_kw={"placeholder": "Enter Full Name"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter Email Address"})
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Verify Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    #Validation of forms
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.lower()).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
    def validate_password(self, password):        
        if not password_strength_ok(password.data):
            raise ValidationError('Password must be atleast 8 chars, and MUST contain Uppercase, Lowercase, Digits and Symbols')    


