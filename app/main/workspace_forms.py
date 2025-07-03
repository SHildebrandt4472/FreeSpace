from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
from app.models import WorkSpace

#Forms for editing users

class WorkspaceEditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Enter Name"})
    description = StringField('Description', validators=[DataRequired()], render_kw={"placeholder": "Enter Description"})
    status = SelectField('Status', choices=WorkSpace.status_choices,coerce=int, validators=[DataRequired()])
    location = StringField('Location', render_kw={"placeholder": "Enter Location"})
    thumbnail = FileField("Image",  validators=[FileAllowed(['jpg', 'png'],  'Allowed file types are jpg, png')])    
    submit = SubmitField('Save')  
    cancel = SubmitField('Cancel')    