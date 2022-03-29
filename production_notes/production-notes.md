# Naming Scheme
Under scores for spaces in EVERYTHIING not camel case or hyphens UNLESS class name, then Capitalized Camel Case

# TODO

## Main Pages
[ ] Commission
[ ] Abstract Stamp
[ ] Payment Stamp
[ ] Campaign Dash
[ ] User Dash
[ ] Set Up Campaign owners
[ ] 400 and 403 error pages
[ ] Set Up Imports
[ ] Set up pay math
[ ] Set Up Exports
    [ ] Set Up Match Select Page

## Production Prep
[ ] Code Clean Up
    [ ] Standardize Naming
[ ] Environment Clean Up
    [ ] Test Start Up Process
    [ ] Test migration process
[ ] Database Backup
    [ ] cron job
### Migration Tests
1. create column
2. migrate
3. create other column 
4. migrate

## Done
[x] Set Up Receipt Import

## Side ToDos
[ ] Set Up Flask Environment
    [ ] Set Up Class Migrations for Tables
[x] Add Campaign Adder
[ ] Fix Campaign Update (Admin)
[ ] Payment Alias for users
[ ] User Dashboard
[ ] Add receipt adder
[ ] Setup Login
    [ ] Owner of campaign
    [ ] Page restrictions
[x] Add sql command executer
[ ] Add password for sql command executer
[ ] User data display page
[ ] Normalize and Organize HTML 
    [ ] Update all the HTML Files
    [ ] Update all the routes
[ ] Figure out searchable multi and regular select  
    [ ] Create custom form select
        [ ] Make that form select validate if it was used
            this replaces the need for a DataRequired() validator on SelectForm()
        [ ] Then pass that data to SelectForm().data
[ ] Get loader in app factory so every time app gets run the default values get included

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
