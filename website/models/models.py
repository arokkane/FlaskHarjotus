from .. import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    created_events = db.relationship('Event')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    event_date = db.Column(db.DateTime(timezone=True), default=func.now())
    application_period = db.Column(db.DateTime(timezone=True), default=func.now())
    application_open = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    applications = db.relationship('EventApplication')
    matches = db.relationship('Match')
    complete = db.Column(db.Boolean, default=False)
    notes = db.Column(db.String(1000))
    def getGameName(self):
        game = Game.query.get(self.game_id)
        return game.name
    
class EventApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    character = db.Column(db.Integer, db.ForeignKey('character.id'))
    notes = db.Column(db.String(1000))
    applied_event = db.Column(db.Integer, db.ForeignKey('event.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    def getCharacter(self):
        char = Character.query.get(self.character)
        return char

class Game(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    icon = db.Column(db.String(150), default="GGST/ggst.png")
    characters = db.relationship('Character')

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    icon = db.Column(db.String(150))
    game = db.Column(db.Integer, db.ForeignKey('game.id'))

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    event = db.Column(db.Integer, db.ForeignKey('event.id'))
    game = db.Column(db.Integer, db.ForeignKey('game.id'))
    player1id = db.Column(db.Integer, db.ForeignKey('player.id'))
    score1 = db.Column(db.Integer, default=0)
    player1_char = db.Column(db.Integer, db.ForeignKey('character.id'))
    player2_char = db.Column(db.Integer, db.ForeignKey('character.id'))
    player2id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player1 = db.relationship("Player", foreign_keys=[player1id])
    player2 = db.relationship("Player", foreign_keys=[player2id])
    score2 = db.Column(db.Integer, default=0)
    match_done = db.Column(db.Boolean, default=False)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))