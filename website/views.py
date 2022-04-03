from importlib.metadata import requires
import json
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
from .forms import MyForm, EventCreationFrom

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short.', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)
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
@views.route('/create-event', methods=['GET', 'POST'])
def create_event():
    form = EventCreationFrom(request.form)
    if request.method == 'POST':
        pass
        #implement event creation
    return render_template("create_event.html", user=current_user, form=form)
@views.route('/application', methods=['GET', 'POST'])
def application():
    form = MyForm()

    if request.method == 'POST':
        pass
        #implement application form
    return render_template("application.html", user=current_user, form=form)