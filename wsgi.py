from website import create_app, db
from website.extensions_inits import load_preset_data
from dataclasses import dataclass
import imbedded as i

<<<<<<< HEAD
=======

>>>>>>> main
def start():
    app = create_app()
    app.app_context().push()
    db.create_all()
    load_preset_data(app, db)

    return app

<<<<<<< HEAD
app = start()

if __name__=='__main__':
=======
if __name__=='__main__':
    app = start()
>>>>>>> main
    app.run()
