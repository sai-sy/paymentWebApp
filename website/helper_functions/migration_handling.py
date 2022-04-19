from ..models.campaigns import Campaigns

'''
Build functions here that will populate the old data up to date with the new features/collumns you're adding and migrating
'''

def all_hex_codes_to_upper():
    '''
    Checks every campaign for a lower case in the hex code, corrects it to uppercase
    '''
    campaign: Campaigns
    for campaign in Campaigns.query.filter_by():
        if [letter for letter in campaign.hex_code if letter is campaign.hex_code.lower()]:
            campaign.hex_code = str(campaign.hex_code).upper()



def run_back_check():
    '''
    Run the checks and corrections declared in this
    '''
    all_hex_codes_to_upper()
    