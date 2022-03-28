from flask import Flask, appcontext_popped, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate

#Path Math
import sys
import os
from . import config

db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "main"

def create_app():
    #Flask Instance
    app = Flask(__name__)
    #app.config.from_pyfile('config.py')
    app.config.from_object(config.ProdConfig)
    
    #Database
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
    #app.config['SECRET_KEY'] = '123'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/main'
    db.init_app(app)
    migrate.init_app(app, db)
    
    #migrate = Migrate(app, db)
    
    with app.app_context():
        from .views import views
        from .auth import auth
        from .campaign_route import campaign_route
        from .shift_route import shift_route

        from .models.campaigns import Campaigns, admins
        from .models.users import Users, SystemLevels
        from .models.people import People
        from .models.shiftstamps import ShiftStamps, Activities
        from .models.admincommands import AdminCommands
        from .models.receipts import Receipts

        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')
        app.register_blueprint(campaign_route, url_prefix='/')
        app.register_blueprint(shift_route, url_prefix='/')

        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)
        login_manager.login_message = "User needs to be logged in to view this page"

        @login_manager.user_loader
        def load_user(id):
            return Users.query.get(int(id))

    return app