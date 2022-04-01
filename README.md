This is a program made for internal use for liberal campaigns to manage volunteer hours and pay

## Contributors
- Saihaan Syed  
- Shakib Ahmed  

### Setting up configuration file
- In class ```DevConfig```, update path for .env file  
- Ensure Git ignores local changes to the config file using the following command:  
    ```git update-index --assume-unchanged <path>``` where ```<path>``` represents the path to config.py

## Running Notes
- Wipe Database using:  
```python  
mycursor.execute(f'DROP DATABASE {name};')  
mycursor.execute(f'CREATE DATABASE {name};')  
```
- Then run the app   
- Then create the database by running ```database_create_all_script()```  
## Server Tips
restart nginx `sudo systemctl restart nginx` 
restart gunicorn `sudo supervisorctl reload`

## Migrations  
### Setting Up 
- CD into payment web app  
- Bash: ```export FLASK_APP=website``` 
- CMD: ```set FLASK_APP=website```  
    ```flask db init```

### Migrate  
```flask db migrate -m 'Message'```  
```flask db upgrade```  
  
  
### Dependencies  
```
pip install dotenv 
  
pip install flask  
pip install flask-wtf
pip install Flask-Migrate 
pip install flask_login 
  
pip install sqlalchemy  
```