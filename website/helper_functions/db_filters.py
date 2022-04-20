from ..models.users import Users
from ..models.campaigns  import Campaign_Contracts, Campaigns
from sqlalchemy import desc
import random

def all_campaigns_user_in(current_user):
    '''
    Returns all the campaigns that a user is a part of
    Returns (value, label) pairs in a list
    '''
    campaign_choices = []
    for c in current_user.campaign_contracts:
        campaign_choices.append((str(c.campaign.id), str(c.campaign.alias)))

    return campaign_choices

def all_campaigns_user_admins(current_user):
    '''
    Returns all the campaigns that a user is an admin of
    Returns (value, label) pairs in a list
    '''
    campaign_choices = []
    for c in current_user.admin_campaigns:
        campaign_choices.append((str(c.id), str(c.alias)))

    return campaign_choices

def all_campaigns_user_admins_list(current_user):
    '''
    Returns a list of all campaigns a user is a part of
    '''
    campaign_choices = []
    for contract in Campaign_Contracts.query.order_by(desc(Campaign_Contracts.user_id)):
        if contract.user_id == current_user.id:
            for campaign in Campaigns.query.order_by(desc(Campaigns.alias)):
                if campaign.id == contract.campaign_id:
                    campaign_choices.append(campaign)
    return campaign_choices

def all_campaigns():
    return [(str(c.id), str(c.alias))  for c in Campaigns.query.order_by(desc(Campaigns.alias))]

def users_in_campaign_user_adminning(current_user):
    '''
    Checks all the campaigns admined by the passed user, and finds all the users in the campaigns he has.
    Returns (value, label) pairs in a list
    '''
    user_choices = []

    for c in current_user.admin_campaigns:
        for u in c.user_contracts:
            tup = (str(u.user_id), str(u.user.first_name + ' ' + u.user.last_name))
            if tup in user_choices:
                continue
            else:
                user_choices.append(tup)

    return user_choices

def admins_in_campaign(campaign_id):
    """
    Returns a list of all the admins in a campaign
    """
    campaign = Campaigns.query.filter(Campaigns.id==campaign_id).first()
    admins = [user for user in campaign.admins]
    return admins

def admins_id_in_campaign(campaign_id):
    """
    Returns a list of all the admins in a campaign
    """
    campaign = Campaigns.query.filter(Campaigns.id==campaign_id).first()
    admins = [user.id for user in campaign.admins]
    return admins

def users_in_campaign(campaign_id):
    """
    Returns a list of all the users contracted under a campaign
    """
    campaign = Campaigns.query.filter(Campaigns.id==campaign_id).first()
    contracts = [contract for contract in campaign.user_contracts]

    users = []
    for contract in contracts:
        users.append(contract.user)
    return users

def rate_for_activity(activity, campaign_id, user_id):
    """
    Checks campaign for activity rates and assigns a rate based on activity
    """
    campaign_contract: Campaign_Contracts = Campaign_Contracts.query.filter_by(user_id=user_id, campaign_id=campaign_id)
    out = float(campaign_contract.pay_rates[activity+'_rates'])
    return out

def uniqueCampaignHex(objectName):
    while(True):
        hex = '%08x' % random.randrange(16**8)
        campaign = objectName.query.filter_by(hex_code=hex).first()
        if campaign:
            continue
        else:
            return hex.upper()

def campaigns_user_administrating(user_id):
    """
    In list format, return the campaigns that user had admin power of
    """
    user = Users.query.filter(Users.id==user_id).first()
    admin = []
    for c in user.admin_campaigns:
        admin.append(c.id)
    return admin