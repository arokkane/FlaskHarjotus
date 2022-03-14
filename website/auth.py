from flask import Blueprint, render_template, request, flash
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html.j2")
@auth.route('/logout')
def logout():
    return "<p>Logout</p>"
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if len(email) < 4:
            flash('Email must be longer than 4 characters', category='error')
        elif len(firstName) < 2:
            flash('First Name must be longer than 2 characters', category='error')
        elif password1 != password2:
            flash('Passwords do\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            new_user = User(email=email, firstName=firstName)
            flash('Account created', category='success')

    return render_template("sign_up.html.j2")