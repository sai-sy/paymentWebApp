# Style Guide
Please preview `/paymentwebapp/README.md`

# TODO  
### Main Pages
- UPDATE DELETE BUTTONS
- [ ] Campaign Dash
    - [ ] Admins
        - [x] lists
        - [ ] remove
        - [ ] add
    - [ ] Shifts
        - [x] List
        - [ ] Edit
        - [x] Add
    - [ ] Payments
        - [ ] List
        - [ ] Edit
        - [ ] Add campaign function to update pay out info
    - [ ] Receipts
        -[x] List
        -[ ] Add
            - [ ] Pay Out
        -[ ] Click thru on receipt to open image of receipt
        -[ ] Let choice of receipt payment or not and add a default bool for that
        -[ ] Edit
            - do not edit the image name!
        -[ ] add accept or deny
    - [ ] User List
        - [x] List
        - [ ] Remove User
        - [ ] Click Name
            - [ ] Opens Profile Info
            - [ ] Contract Info On Right
            - [ ] Change Contract btn IF ADMIN, View Shifts, View Paystampts, View Receipts, View Abstracts
        - [ ] User Contract
            - [ ] Apply to certain a certain date back
            - [ ] Any changes to the getting paid values need to go in and update the campaign object output
            - [x] Display all contract values
    - [ ] Create Output
        - [x] Create the output
    - [ ] Intuitive way to edit campaign properties
        - [x] Campaign Heading Info
        - [ ] Campaign Pay Info
            - [ ] Update every contract to be minimum changed rates
    - [ ] show personal contract on right (wait)
    - [ ] Way to change the contract to get people paid
                - [ ] MASS CHANGES TO PEOPLE GETTING PAID
                    - [ ] Change users getting paid button (seperate from edit user contract button) (maybe make it in the edit pay for campaign page)
                    - [ ] after submit button make a list of all the users
                    - [ ] checkbox checked or not based on if they get paid or not
                - [ ] (Future might need ajax) Toggle switch for getting paid that live updates the database





- [ ] Output backend
    - [ ] Make each paystamp include an activity drop down
    - [ ] Make the backend math use that dropdown

- [ ] Try Catch in auth.signup  
    - This try-except is made to work for unique alias'  
        - Desc: If something else throws that error, it'll get stuck in an infinite loop. There needs to be a better solution for this  
        - Solutions:  
            - make a program that will throw an error, see what the error is, parse it and do things for specifc attributes  
            - https://stackoverflow.com/questions/11313490/how-to-find-the-offending-attribute-with-a-sqlalchemy-integrityerror  
- [ ] Receipts File Directory pointing manually not off of config file  
- [ ] Self-Referential Many-to-Many relationship for commission  
- [ ] Pay Infrustructure  
    - [x] Attatch a rate to each campaign  
    - [x] Attatch a rate to each shift  
    - [ ] Make the shift rate based on the campaign rate  
    - [ ] retroactive pay change on output report  
- [X] Imports  
    - [x] Front End  
    - [X] Back End  
- [ ] Exports  
    - [ ] Front End  
    - [ ] Back End  
    - [ ] Bulk Export
        - [ ] Naming scheme: Date Added_Version

- [ ] Campaign List
    - [x] Filter campaigns by admin/ownership status
    - [x] Campaign links redirect to campaign dashboard  
        - [ ] Include campaign link functionality on user dash
- [ ] Receipt Display  

    - [ ] display shifts
        - [ ] if they are being paid for that campaign, let them see some numbers
- [ ] Set Up Campaign owners and auto admin  
- [ ] Error pages   
    - [x] 403  
    - [x] 404  
    - [x] 500  
    - [ ] 400  
    - [ ] 512
    - [x] absolute or relative path in production notes git ignore config file section @sshakibbb  

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
- [x] Campaign Ownership  
    - [x] Each Campaign Should Create a code and have a many-to-many relationship with users  
- [x] Abstract Stamp  
- [x] Payment Stamp  
- [x] User alias  
- [x] Commission  
- [x] Git ignore contents of upload folder, not file structure
- [x] Make owner a part of campaign they created with a contract 
- [x] Change the way admins are created


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
