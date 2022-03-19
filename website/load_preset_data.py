from ast import Try

from mysqlx import IntegrityError
from .models.shiftstamp import Activities
from .models.users import Users, SystemLevels
from sqlalchemy import exc

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
    with app.app_context():
        adder(app, db, calling)
        adder(app, db, canvas)
        adder(app, db, litdrop)
        adder(app, db, admin)
