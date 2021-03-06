# IMPORT MODELS
from .models.shiftstamps import Activities
from .models.users import Users, SystemLevels
from .models.admincommands import AdminPassword
from .models.campaigns import GovLevels

from sqlalchemy import exc, over
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
    canvas = Activities(activity="canvass")
    litdrop = Activities(activity="litdrop")
    admin = Activities(activity="admin")
    general = Activities(activity="general")
    overall = Activities(activity="overall")
    with app.app_context():
        adder(app, db, calling)
        adder(app, db, canvas)
        adder(app, db, litdrop)
        adder(app, db, admin)
        adder(app, db, general)
        adder(app, db, overall)

    # ADD GOVERNMENT LEVELS
    federal = GovLevels(level="Federal")
    federal_nomination = GovLevels(level="Federal Nomination")
    provincial = GovLevels(level="Provincial")
    provincial_nomination = GovLevels(level="Provincial Nomination")
    munical = GovLevels(level="Municipal")
    with app.app_context():
        adder(app, db, federal)
        adder(app, db, federal_nomination)
        adder(app, db, provincial)
        adder(app, db, provincial_nomination)
        adder(app, db, munical)


    # ADD SQL ACCESS PASSWORD
    admin_password = AdminPassword(password=generate_password_hash('alexSpears'))
    with app.app_context():
        adder(app, db, admin_password)
