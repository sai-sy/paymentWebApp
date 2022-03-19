from website import db, create_app
from website.load_preset_data import load_preset_data

app = create_app()
app.app_context().push()
db.create_all()
load_preset_data(app, db)