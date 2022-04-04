from .. import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    created_events = db.relationship('Event')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    event_date = db.Column(db.DateTime(timezone=True), default=func.now())
    application_period = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    applications = db.relationship('EventApplication')
    def getGameName(self):
        game = Game.query.get(self.game_id)
        return game.name

class EventApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    character = db.Column(db.String(150))
    notes = db.Column(db.String(1000))
    applied_event = db.Column(db.Integer, db.ForeignKey('event.id'))

class Game(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    icon = db.Column(db.String(150))
    characters = db.relationship('Character')

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    icon = db.Column(db.String(150))
    game = db.Column(db.Integer, db.ForeignKey('game.id'))
