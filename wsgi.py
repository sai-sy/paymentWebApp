from website import create_app, db
from website.extensions_inits import load_preset_data

def start(name):
    app = create_app(name)
    app.app_context().push()
    db.create_all()
    load_preset_data(app, db)
    return app

app = start(__name__)

if __name__=='__main__':
    app.run(host='0.0.0.0')