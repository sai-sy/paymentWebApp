from flask import Flask, appcontext_popped, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    global app
    app.config['SECRET_KEY'] = 'abc'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

#ERROR HANDLING

@app.errorhandler(404)
def page_not_found(e):
    '''Invalid URL'''
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    '''Internal Server Error'''
    return render_template("500.html"), 500