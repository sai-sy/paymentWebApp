# Naming Scheme
Under scores for spaces in EVERYTHIING not camel case or hyphens UNLESS class name, then Capitalized Camel Case

# TODO
[ ] Set Up Flask Environment
    [ ] Set Up Class Migrations for Tables
[x] Add Campaign Adder
[ ] Fix Campaign Update (Admin)
[ ] Add receipt adder
[ ] Setup Login
    [ ] Owner of campaign
    [ ] Page restrictions
[ ] Add sql command executer
[ ] User data display page
[ ] Normalize and Organize HTML 
    [ ] Update all the HTML Files
    [ ] Update all the routes
[ ] Create custom form select
    [ ] Make that form select validate if it was used
        this replaces the need for a DataRequired() validator on SelectForm()
    [ ] Then pass that data to SelectForm().data
[ ] Get loader in app factory so every time app gets run the default values get included

# Notes

## Setting Up Flask Environment
Flask Fridays Codemy Episode 1 and Episode 11

## Mapping Flask Models to Inheritance
https://docs.sqlalchemy.org/en/14/orm/inheritance.html
We're using joined table inheritance

## Updating Models
### On Startup
When you run the app, you need to make sure all the tables for each model has been built
https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/


# Migration Tools
https://www.youtube.com/watch?v=ca-Vj6kwK7M&list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz&index=11
