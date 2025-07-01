
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

#Forms for login and registration
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Enter Username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    registration_code = StringField('Registration Code', validators=[DataRequired()], render_kw={"placeholder": "Enter Registration Code"})
    username = StringField('Username/Login', validators=[DataRequired()], render_kw={"placeholder": "Enter Username"})
    display_name = StringField('Full Name', validators=[DataRequired()], render_kw={"placeholder": "Enter Full Name"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter Email Address"})
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Verify Password', validators=[DataRequired(), EqualTo('password')])
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

