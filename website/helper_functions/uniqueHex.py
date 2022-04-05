import random

def uniqueCampaignHex(objectName):
    while(True):
        hex = '%08x' % random.randrange(16**8)
        campaign = objectName.query.filter_by(hex_code=hex).first()
        if campaign:
            continue
        else:
            return hex