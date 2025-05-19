from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,DateTimeField, BooleanField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import Slot


class SlotEditForm(FlaskForm):

    #start_time = DateTimeField("Start time", validators=[DataRequired()])
    start_time = DateTimeLocalField('Start Time', validators=[DataRequired()])
    duration = SelectField('Duration', choices=Slot.duration_choices, coerce=int, validators=[DataRequired()])
    description = StringField('Description')
    repeating = BooleanField("Repeating")
    submit = SubmitField('Save')

<<<<<<< HEAD
class SlotBookingForm(FlaskForm):

    #start_time = DateTimeField("Start time", validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Book')
=======
>>>>>>> eb0827f242874b22139aa8d4d1c704437dc3b092
