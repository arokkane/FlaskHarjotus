from datetime import datetime
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .models.models import Character, Game, EventApplication, Match, Player, Event
from . import db
from .forms import AddMatch, ApplicationForm, Modifyform, EventCreationForm


event = Blueprint('event', __name__)
@login_required
@event.route('/create-event', methods=['GET', 'POST'])
def create_event():
    form = EventCreationForm()
    #print(form.validate())
    #flash(form.errors)
    if form.validate_on_submit():
        chosen_game = Game.query.get(form.game.data)
        new_event = Event(
            name=form.name.data,
            game_id=chosen_game.id,
            event_date = form.event_time.data,
            application_period = form.application_period.data,
            user_id=current_user.id)
        db.session.add(new_event)
        db.session.commit()
        flash('Event added!', category='success')
        return redirect(url_for('views.home'))
    return render_template("create_event.html", user=current_user, form=form)
@event.route('/application', methods=['GET', 'POST'])
def application():
    eventid = request.args.get('id')
    event = Event.query.get(eventid)
    form = ApplicationForm()
    form.character.choices = [(character.id, character.name)for character in Character.query.filter_by(game=event.game_id).all()]
    if form.validate_on_submit():
        player_name = form.name.data
        if (Player.query.filter_by(name = player_name).first() == None):
            new_player = Player(
                name=form.name.data
            )
            db.session.add(new_player)
            db.session.commit()
        new_application = EventApplication(
            name=form.name.data,
            character = form.character.data,
            notes = form.notes.data,
            applied_event = eventid,
            player_id = Player.query.filter_by(name = player_name).first().id
        )
        
        db.session.add(new_application)
        db.session.commit()
        return redirect(url_for('views.home'))

    return render_template("application.html", user=current_user, form=form, event=event)
    
@login_required
@event.route('/manage-event', methods=['GET', 'POST'])
def manage_event():

    eventid = request.args.get('id')
    event = Event.query.get(eventid)
    form = Modifyform(name=event.name, game=event.game_id, event_time=event.event_date, application_period = event.application_period)
    if form.validate_on_submit():
        chosen_game = Game.query.get(form.game.data)
        event.name=form.name.data
        event.game_id=chosen_game.id
        event.event_date = form.event_time.data
        print(form.application_period.data)
        event.application_period = form.application_period.data
        if (form.close_applications.data):
            event.application_open = False
            flash('Applications closed!', category='success')
        db.session.commit()
        flash('Event modified!', category='success')

    applications = []
    for a in event.applications:
        applications.append((a, a.getCharacter()))
    return render_template("manage_event.html", 
        user=current_user, 
        event=event, 
        applications=applications, 
        form=form)

@event.route("/eventdata",methods=["POST","GET"])
def applicantdata():
    if request.method == 'POST':
        userid = request.form['userid']
        print(userid)
        eventdata = Event.query.get(userid)
        
    return jsonify({'htmlresponse': render_template('eventmodal.html', event=eventdata)})   

@event.route("/view-event", methods=['POST', 'GET'])
def view_event():
    eventid = request.args.get('id')
    event = Event.query.get(eventid)
    choosable_players = [] 
    for application in event.applications:
        choosable_players.append((application.player_id, application.name))
    form = AddMatch()
    form.player1.choices = choosable_players
    form.player2.choices = choosable_players
    characters = Character.query.filter_by(game = event.game_id).all()
    characterlist = [0] * 1000
    for character in characters:
        characterlist[character.id] = character
    if form.validate_on_submit():
        player1_char = player2_char = 0
        for application in event.applications:
            if application.player_id == int(form.player1.data):
                player1_char = application.character
            if application.player_id == int(form.player2.data):
                player2_char = application.character
            
        new_match = Match(
            date = event.event_date,
            event = event.id,
            game = event.game_id,
            player1id = form.player1.data,
            score1 = form.score1.data,
            player1_char = player1_char,
            player2_char = player2_char,
            player2id = form.player2.data,
            score2 = form.score2.data,
            )
        db.session.add(new_match)
        db.session.commit()
        flash('Match Added!', category='success')
    return render_template("event.html", 
        user=current_user,
        event=event, 
        form=form,
        characters=characterlist)