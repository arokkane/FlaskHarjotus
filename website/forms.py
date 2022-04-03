from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired, InputRequired, Length
GAME_CHOICES = [('0', 'Guilty Gear Strive'),('1', 'BlazBlue Centralfiction'), ('2', 'Street Fighter V0')]

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

class EventCreationFrom(FlaskForm):
    name = StringField('Event Name', validators=[InputRequired(), Length(min=1, max=200)])
    game = SelectField(label='Select Game', choices=GAME_CHOICES)
    application_period = DateTimeLocalField(label='Application Period', validators=[InputRequired()])
    event_time = DateTimeLocalField(label='Event Date', validators=[InputRequired()])