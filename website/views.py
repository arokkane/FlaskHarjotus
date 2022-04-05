from datetime import datetime
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .models.models import Character, Game, EventApplication, Player, Event
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