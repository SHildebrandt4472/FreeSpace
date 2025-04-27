from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import WorkSpace

#Forms for editing users

class WorkspaceEditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices=WorkSpace.status_choices,coerce=int, validators=[DataRequired()])
    location = StringField('Location')
    submit = SubmitField('Save')
