import inspect
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask import Flask, render_template, redirect, url_for


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config.from_object('website.config.DevelopmentConfig')
    db.init_app(app)
    

    with app.app_context():
        from .views import views
        from .auth import auth
        from .event import event
        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')
        app.register_blueprint(event, url_prefix='/')

        from .models.models import User, Event, Game, Character
        #create_database(app)
        db.create_all(app=app)
        print('Created Database')

        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(id):
            return User.query.get(int(id))

        return app

def create_database(app):
    if not path.exists('website/database/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database')


