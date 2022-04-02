from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired
GAME_CHOICES = [('0', 'Guilty Gear Strive'),('1', 'BlazBlue Centralfiction'), ('3', 'Street Fighter V0')]

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

class EventCreationFrom(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    game = SelectField(label='Select Game', choices=GAME_CHOICES)