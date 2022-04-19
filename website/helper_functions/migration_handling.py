from flask import current_app
from ..models.campaigns import Campaigns
from .. import db

'''
Build functions here that will populate the old data up to date with the new features/collumns you're adding and migrating
'''

def all_hex_codes_to_upper():
    '''
    Checks every campaign for a lower case in the hex code, corrects it to uppercase
    '''
    current_app.logger.info('enter hex code func')
    campaign: Campaigns
    for campaign in Campaigns.query.filter_by():
        if [letter for letter in campaign.hex_code if letter.islower()]:
            campaign.hex_code = str(campaign.hex_code).upper()
    db.session.commit()



def run_back_check():
    '''
    Run the checks and corrections declared in this
    '''
    current_app.logger.info('enter run back check func')
    all_hex_codes_to_upper()
    