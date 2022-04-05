from datetime import datetime
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .models.models import Character, Match, EventApplication, Player, Event
from . import db
from .forms import ApplicationForm, Modifyform,  EventCreationForm

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
def home():
    events = Event.query.all()
    eventlist = []
    for e in events:
        game_name = e.getGameName()
        if e.application_period < datetime.now(e.application_period.tzinfo):
            application_open = False
        else:
            application_open = True
        eventlist.append((e, game_name, application_open))

    return render_template("home.html", user=current_user, events=eventlist)


@views.route("/applicantdata",methods=["POST","GET"])
def applicantdata():
    if request.method == 'POST':
        userid = request.form['userid']
        print(userid)
        applicationdata = EventApplication.query.get(userid)
        
    return jsonify({'htmlresponse': render_template('applymodal.html',applications=applicationdata)})   

@views.route("/matches", methods=['GET'])
def matches():
    matches = Match.query.all()
    characters = Character.query.all()
    characterlist = [0] * 1000
    for character in characters:
        characterlist[character.id] = character

    return render_template("matches.html", user=current_user, matches=matches, characters=characterlist)

@views.route("/guilty-gear", methods=['GET'])
def guilty_gear():
    characters = Character.query.filter_by(game=1).all()
    data = []
    for character in characters:
        matches = Match.query.all()
        games = 0
        for match in matches:
            if match.player1_char == character.id or match.player2_char == character.id:
                games += 1
        data.append((character, games)) 
    Sort_Tuple(data)
    return render_template("guilty_gear.html", user=current_user, data=data)

@views.route("/blazblue", methods=['GET'])
def blazblue():
    characters = Character.query.filter_by(game=2).all()
    data = []
    for character in characters:
        matches = Match.query.all()
        games = 0
        for match in matches:
            if match.player1_char == character.id or match.player2_char == character.id:
                games += 1
        data.append((character, games)) 
    Sort_Tuple(data)
    return render_template("blazblue.html", user=current_user, data=data)

@views.route("/players", methods=['GET'])
def players():
    players = Player.query.all()
    data = []
    for player in players:
        matches = Match.query.all()
        games = 0
        for match in matches:
            if match.player1id == player.id or match.player2id == player.id:
                games += 1
        data.append((player, games)) 
    Sort_Tuple(data)
    return render_template("players.html", user=current_user, data=data)

def Sort_Tuple(tup): 
  
    # reverse = None (Sorts in Ascending order) 
    # key is set to sort using second element of 
    # sublist lambda has been used 
    tup.sort(key = lambda x: x[1], reverse=True) 
    return tup 