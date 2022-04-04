from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField, DateTimeLocalField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length
GAME_CHOICES = [('1', 'Guilty Gear Strive'),('2', 'BlazBlue Centralfiction'), ('3', 'Street Fighter V')]

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

class EventCreationForm(FlaskForm):
    name = StringField(label='Event Name', validators=[InputRequired(), Length(min=1, max=200)])
    game = SelectField(label='Select Game', choices=GAME_CHOICES, validators=[InputRequired()])
    event_time = DateTimeLocalField(label='Event Date', validators=[InputRequired()],format='%Y-%m-%dT%H:%M')
    application_period = DateTimeLocalField(label='Application Period', validators=[InputRequired()], format='%Y-%m-%dT%H:%M')
    submit = SubmitField(label='Submit')

class ApplicationForm(FlaskForm):
    name = StringField(label='Name', validators=[InputRequired(), Length(min=1, max=200)])
    character = SelectField('Character', choices=[])
    notes = TextAreaField('Additional notes')
    submit = SubmitField(label='Submit')