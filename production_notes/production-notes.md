# Style Guide
Please preview /paymentwebapp/README.md

# TODO  
### Main Pages  
- [ ] Commission  
- [ ] Pay Infrustructure
- [ ] Imports
    - [ ] Front End
    - [ ] Back End
- Exports
    - [ ] Front End
    - [ ] Back End
- [ ] Abstract Stamp  
- [ ] Payment Stamp  
- [ ] Campaign Dash  
- [ ] Receipt Display
- [ ] User Dash  
    - [ ] Top is a box that displays all content  
    - [ ] if admin  
        - [ ] have edit buttons  
        - [ ] have add commission feed button  
        - [ ] have add commisson receieve button  
- [ ] Set Up Campaign owners and auto admin  
- [ ] 400 and 403 error pages   
- absolute or relative path in production notes git ignore config file section @sshakibbb

### Production Prep  
- [ ] Code Clean Up  
    - [ ] Standardize Naming  
- [ ] Environment Clean Up  
    - [ ] Test Start Up Process  
    - [ ] Test migration process  
- [ ] Database Backup  
    - [ ] cron job  

## Done  
- [x] Set Up Receipt Import 

### Migration Tests  
1. create column  
2. migrate  
3. create other column  
4. migrate  

# Development Setup
### Get the personal config file git ignored
- In class ```DevConfig```, update path for .env file  
- Ensure Git ignores local changes to the config file using the following command:  
    ```git update-index --assume-unchanged <path>``` where ```<path>``` represents the path to config.py
  
## Side ToDos  
- [ ] Set Up Flask Environment  
    - [ ] Set Up Class Migrations for Tables  
- [x] Add Campaign Adder  
- [ ] Fix Campaign Update (Admin)  
- [ ] Payment Alias for users  
- [ ] User Dashboard  
- [ ] Add receipt adder  
- [ ] Setup Login  
    - [ ] Owner of campaign  
    - [ ] Page restrictions  
- [x] Add sql command executer  
- [ ] Add password for sql command executer  
- [ ] User data display page  
- [ ] Normalize and Organize HTML  
    - [ ] Update all the HTML Files  
    - [ ] Update all the routes  
- [ ] Figure out searchable multi and regular select   
    - [ ] Create custom form select  
        - [ ] Make that form select validate if it was used  
            - this replaces the need for a DataRequired() validator on SelectForm()  
        - [ ] Then pass that data to SelectForm().data  
- [ ] Get loader in app factory so every time app gets run the default values get included  
  
# Notes  
  
## Setting Up Flask Environment  
Flask Fridays Codemy Episode 1 and Episode 11  
https://hackersandslackers.com/configure-flask-applications/  
  
## Mapping Flask Models to Inheritance  
https://docs.sqlalchemy.org/en/14/orm/inheritance.html  
We're using joined table inheritance  
  
## Updating Models  
### On Startup  
When you run the app, you need to make sure all the tables for each model has been built  
https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/  
  
  
# Migration Tools  
https://www.youtube.com/watch?v=ca-Vj6kwK7M&list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz&index=11  
