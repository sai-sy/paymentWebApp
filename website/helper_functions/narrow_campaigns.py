from ..models.campaigns  import Campaigns
from sqlalchemy import desc

def all_campaigns_user_in(current_user):
    '''
    Returns all the campaigns that a user is a part of
    Returns (value, label) pairs in a list
    '''
    campaign_choices = []
    for c in Campaigns.query.order_by(desc(Campaigns.alias)):
        for u in c.users_under:
            if u.id == current_user.id:
                campaign_choices.append((str(c.id), str(c.alias)))

    return campaign_choices

def all_campaigns_user_admins(current_user):
    '''
    NOT WORKING!!!!
    '''
    campaign_choices = []
    for c in Campaigns.query.order_by(desc(Campaigns.alias)):
        for u in c.users_under:
            if u.id == current_user.id:
                campaign_choices.append((str(c.id), str(c.alias)))

    return campaign_choices

def users_in_campaign_under_user(current_user):
    '''
    Checks all the campaigns under the passed user, and finds all the users in the campaigns he has.
    Returns (value, label) pairs in a list
    '''
    user_choices = []

    for c in current_user.campaigns_under:
        for u in c.users_under:
            tup = (str(u.id), str(u.first_name + ' ' + u.last_name))
            if tup in user_choices:
                continue
            else:
                user_choices.append(tup)

    return user_choices