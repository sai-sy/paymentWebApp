from flask import current_app
from ..models.campaigns import Campaigns
from .. import db
from .. import celery

import threading
import requests

'''
Build functions here that will populate the old data up to date with the new features/collumns you're adding and migrating
'''

def all_hex_codes_to_upper():
    '''
    Checks every campaign for a lower case in the hex code, corrects it to uppercase
    '''
    campaign: Campaigns
    for campaign in Campaigns.query.filter_by():
        if [letter for letter in campaign.hex_code if letter.islower()]:
            campaign.hex_code = str(campaign.hex_code).upper()
    db.session.commit()
    current_app.logger.info('Done Hex Code To Upper Process')

@celery.task(name='app.tasks.campaign_pay_out_process')
def campaign_pay_out_process():
    '''
    Process Every Campaigns Pay
    '''
    campaign: Campaigns
    for campaign in Campaigns.query.filter_by():
        campaign.process_pay()
    db.session.commit()
    current_app.logger.info('Done Campaign Pay Out Processing')



def run_back_check():
    '''
    Run the checks and corrections declared in this
    '''
    current_app.logger.info('Running First Request Checks')
    all_hex_codes_to_upper()
    threading.stack_size(7000000)
    #threading.Thread(target=campaign_pay_out_process).start()
    campaign_pay_out_process.apply_aysnc(args=[])
    