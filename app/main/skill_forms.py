from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, HiddenField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import Skill

class SkillForm(FlaskForm):        
    description = StringField('Description', validators=[DataRequired()], render_kw={"placeholder": "Description"})
    submit = SubmitField('Update') 
    