from ..models.campaigns  import Campaigns
from sqlalchemy import desc

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
    for c in Campaigns.query.order_by(desc(Campaigns.alias)):
        for u in c.users_under:
            if u.id == current_user.id:
                campaign_choices.append(c)
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