from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

#Forms for editing users

class UserEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    display_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    access = SelectField('Access Level', choices=[(10, 'Student'), (20, 'Staff'), (30, 'Manager'), (40, 'Admin')],coerce=int, validators=[DataRequired()])
    submit = SubmitField('Register')

    #Validation of forms

    #def validate_email(self, email):
    #    user = User.query.filter_by(email=email.data).first()
    #    if user is not None and user.username != self.username:
    #        raise ValidationError('Please use a different email address.')

