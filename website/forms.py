from secrets import choice
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField, DateTimeLocalField, TextAreaField, IntegerField, FormField, FieldList
from wtforms.validators import DataRequired, InputRequired, Length
GAME_CHOICES = [('1', 'Guilty Gear Strive'),('2', 'BlazBlue Centralfiction'), ('3', 'Street Fighter V')]

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

class Modifyform(EventCreationForm):
    close_applications = SubmitField(label='Close applications')

class AddMatch(FlaskForm):
    player1 = SelectField(label='Player 1', choices=[])
    score1 = IntegerField(label='Score 1')
    player2 = SelectField(label='Player 2', choices=[])
    score2 = IntegerField(label='Score 2')
    submit = SubmitField(label='Add Match')

class MatchesForm(FlaskForm):
    matches = FieldList(FormField(AddMatch), min_entries=1)