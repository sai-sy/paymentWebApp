from website import create_app, db
from dataclasses import dataclass
import imbedded as i

db_holder = db

app = create_app()
app.config['SECRET_KEY'] = i.s.scrt_key

if __name__=='__main__':
    app.run(debug=True)
