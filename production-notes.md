## Mapping Flask Models to Inheritance
https://docs.sqlalchemy.org/en/14/orm/inheritance.html
We're using joined table inheritance

## Updating Models
# On Startup
When you run the app, you need to make sure all the tables for each model has been built
https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
```python
>>> from website import db, create_app
>>> app = create_app()
>>> app.app_context().push()
>>> db.create_all()
```

# Migration Tools
https://www.youtube.com/watch?v=ca-Vj6kwK7M&list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz&index=11
