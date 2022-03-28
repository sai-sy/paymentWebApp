from ast import Try

from mysqlx import IntegrityError
from .models.shiftstamps import Activities
from .models.users import Users, SystemLevels
from .models.admincommands import AdminPassword
from sqlalchemy import exc
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash

def adder(app, db, add):
    try:
        with app.app_context():
            db.session.add(add)
            return db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()

def load_preset_data(app, db):
    
    # ADD SYSTEM LEVELS
    ground = SystemLevels(level="GROUND", numeric_level=1)
    mod = SystemLevels(level="MOD", numeric_level=4)
    serverking = SystemLevels(level="SERVERKING", numeric_level=10)
    with app.app_context():
        adder(app, db, ground)
        adder(app, db, mod)
        adder(app, db, serverking)

    # ADD ACTIVITES
    calling = Activities(activity="calling")
    canvas = Activities(activity="canvas")
    litdrop = Activities(activity="litdrop")
    admin = Activities(activity="admin")
    general = Activities(activity="general")
    with app.app_context():
        adder(app, db, calling)
        adder(app, db, canvas)
        adder(app, db, litdrop)
        adder(app, db, admin)
        adder(app, db, general)

    # ADD SQL ACCESS PASSWORD
    admin_password = AdminPassword(password=generate_password_hash('alexSpears'))
    with app.app_context():
        adder(app, db, admin_password)
