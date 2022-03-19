from datetime import datetime, time

def getLabel(minute, hour):
    label = ''
    if hour < 12:
        if minute < 10:
            return label + str(hour) + ':' + '0' + str(minute) + ' AM'
        else:
            return label + str(hour) + ':' + str(minute) + ' AM'
    else:
        if minute < 10:
            return label + str(hour-12) + ':' + '0' + str(minute) + ' PM'
        else:
            return label + str(hour-12) + ':' + str(minute) + ' PM'

def listoftimes():
    hours = [4+12, 5+12, 6+12, 7+12, 8+12, 9+12, 10+12, 11+12, 12+12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1+12, 2+12, 3+12]
    minutes = [0, 15, 30 , 45]
    output = []
    for hour in hours:
        label = ''
        for minute in minutes:
            if hour == 24:
                output.append((time(hour=0, minute=minute), getLabel(minute, hour)))
            elif hour > 12:
                output.append((time(hour=hour, minute=minute), getLabel(minute, hour)))
            else:
                output.append((time(hour=hour, minute=minute), getLabel(minute, hour)))
    return output