from website import create_app, db
from db_startup import start
from dataclasses import dataclass
import imbedded as i

app = start()
#app = create_app()
app.config['SECRET_KEY'] = i.s.scrt_key

if __name__=='__main__':
    app.run()
