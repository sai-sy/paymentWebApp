This is a program made for internal use for liberal campaigns to manage volunteer hours and pay

## Contributors
Saihaan Syed  
Shakib Ahmed  

## Running Notes
Wipe Database using  
```python  
mycursor.execute(f'DROP DATABASE {name};')  
mycursor.execute(f'CREATE DATABASE {name};')  
```
Then run the app   
Then create the database by running database_create_all_script()  

## Migrations  
### Setting Up 
CD into payment web app  
Bash: export FLASK_APP=website 
CMD: set FLASK_APP=website  
flask db init  
### Migrate  
flask db migrate -m 'Message'  
flask db upgrade  
  
  
### Dependencies  
```
pip install dotenv  
  
pip install flask  
pip install Flask-Migrate  
pip install flask_login  
  
  
pip install sqlalchemy  
```