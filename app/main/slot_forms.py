from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,DateTimeField, BooleanField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import Slot


class SlotEditForm(FlaskForm):

    #start_time = DateTimeField("Start time", validators=[DataRequired()])
    start_time = DateTimeLocalField('Start Time', validators=[DataRequired()])
    duration = SelectField('Duration', choices=Slot.duration_choices, validators=[DataRequired()])
    description = StringField('Description')
    repeating = BooleanField("Repeating")
    submit = SubmitField('Save')

