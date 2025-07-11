from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,IntegerField, HiddenField, PasswordField
from wtforms.validators import DataRequired, Optional, ValidationError, Email, EqualTo
from app.models import User
from sqlalchemy import and_
from .login_forms import password_strength_ok


#Forms for editing users

class UserEditForm(FlaskForm):
    id = HiddenField('Id') # used in validation
    username = StringField('Username', validators=[DataRequired()])
    display_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    access = SelectField('Access Level', choices=[(10, 'Student'), (20, 'Staff'), (30, 'Manager'), (40, 'Admin')],coerce=int,validators=[Optional()])
    submit = SubmitField('Save')
    reset_password = SubmitField('Reset Password', render_kw={'onclick':"return customConfirm('Reset User\\\'s Password?', event)"})

    #Validation of forms      
    def validate_username(self, username):        
        user = User.query.filter(and_(User.username == username.data.lower(), User.id != self.id.data)).first()        
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter(and_(User.email == email.data.lower(), User.id != self.id.data)).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password')
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Verify Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Save')

    def validate_password(self, password):        
        if not password_strength_ok(password.data):
            raise ValidationError('Password must be atleast 8 chars, and MUST contain Uppercase, Lowercase, Digits and Symbols')    