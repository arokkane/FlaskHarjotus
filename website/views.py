from datetime import datetime
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .models.models import Character, Game, Note, EventApplication
from .models.models import Event
from . import db
from .forms import ApplicationForm, MyForm, EventCreationForm

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
def home():
#    if request.method == 'POST':
#        note = request.form.get('note')
#        if len(note) < 1:
#            flash('Note is too short.', category='error')
#        else:
#            new_note = Note(data=note, user_id=current_user.id)
#            db.session.add(new_note)
#            db.session.commit()
#            flash('Note added!', category='success')
    events = Event.query.all()
    eventlist = []
    for e in events:
        game_name = e.getGameName()
        if e.application_period < datetime.now():
            application_open = False
        else:
            application_open = True
        eventlist.append((e, game_name, application_open))

    return render_template("home.html", user=current_user, events=eventlist)
@views.route('/delete-note', methods=['POST'])
def delete_note():
    id = int(request.form.get('id'))
    note = Note.query.get(id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note Deleted', category="success")

    return redirect(url_for('views.home'))
@login_required
@views.route('/create-event', methods=['GET', 'POST'])
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
@views.route('/application', methods=['GET', 'POST'])
def application():
    eventid = request.args.get('id')
    event = Event.query.get(eventid)
    form = ApplicationForm()
    form.character.choices = [(character.id, character.name)for character in Character.query.filter_by(game=event.game_id).all()]
    if form.validate_on_submit():
        new_application = EventApplication(
            name=form.name.data,
            character = form.character.data,
            notes = form.notes.data,
            applied_event = eventid
        )
        db.session.add(new_application)
        db.session.commit()
        flash('Application received!', category='success')
        return redirect(url_for('views.home'))

    return render_template("application.html", user=current_user, form=form, event=event)
    
@login_required
@views.route('/manage-event', methods=['GET', 'POST'])
def manage_event():
    eventid = request.args.get('id')
    event = Event.query.get(eventid)
    return render_template("manage_event.html", user=current_user, event=event)