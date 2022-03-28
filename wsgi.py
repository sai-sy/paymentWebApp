from website import create_app, db
from website.extensions_inits import load_preset_data

def start():
    app = create_app()
    app.app_context().push()
    db.create_all()
    load_preset_data(app, db)

    return app

if __name__=='__main__':
    app = start()
    app.run()