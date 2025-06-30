from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,DateTimeField, BooleanField, FileField, TextAreaField, DateField, HiddenField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import Slot


class SlotEditForm(FlaskForm):    

    #start_time = DateField('Start Time', validators=[DataRequired()])
    day = HiddenField('Hidden Date') 
    hour = SelectField("Hour", choices=Slot.hour_choices, coerce=int)
    minute = SelectField("Minutes", choices=Slot.minute_choices, coerce=int)
    duration = SelectField('Duration (mins)', choices=Slot.duration_choices, coerce=int, validators=[DataRequired()])
    description = TextAreaField('Description')
    repeating = BooleanField("Repeating")      
    submit = SubmitField('Save')

class SlotBookingForm(FlaskForm):    
    description = StringField('Description')
    submit = SubmitField('Book')
    cancel = SubmitField('Cancel')
