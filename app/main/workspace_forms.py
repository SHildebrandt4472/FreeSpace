from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
from app.models import WorkSpace

#Forms for editing users

class WorkspaceEditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices=WorkSpace.status_choices,coerce=int, validators=[DataRequired()])
    location = StringField('Location')
    thumbnail = FileField("Image",  validators=[FileAllowed(['jpg', 'png'],  'Allowed file types are jpg, png')])    
    submit = SubmitField('Save')      