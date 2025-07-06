from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,DateTimeField, BooleanField, FileField, TextAreaField, DateField, HiddenField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import Slot


class SlotEditForm(FlaskForm):        
    day = HiddenField('Hidden Date') 
    hour = SelectField("Hour", choices=Slot.hour_choices, coerce=int)
    minute = SelectField("Minutes", choices=Slot.minute_choices, coerce=int)
    duration = SelectField('Duration (mins)', choices=Slot.duration_choices, coerce=int, validators=[DataRequired()])    
    repeating = BooleanField("Repeat Weekly")      
    submit = SubmitField('Update')

class SlotBookingForm(FlaskForm):    
    description = TextAreaField('Description', render_kw={'rows':5, 'placeholder':'Descripe your planned project here'})
    submit = SubmitField('Update')
    cancel = SubmitField('Cancel')
