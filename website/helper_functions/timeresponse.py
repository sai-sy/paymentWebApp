from datetime import datetime, time

def getLabel(minute, hour):
    label = ''

    if hour == 0:
        if minute < 10:
            return label + '12' + ':' + '0' + str(minute) + ' AM'
        else:
            return label + '12' + ':' + str(minute) + ' AM'     

    if hour == 12:
        if minute < 10:
            return label + '12' + ':' + '0' + str(minute) + ' PM'
        else:
            return label + '12' + ':' + str(minute) + ' PM'       

    if hour < 12:
        if minute < 10:
            return label + str(hour) + ':' + '0' + str(minute) + ' AM'
        else:
            return label + str(hour) + ':' + str(minute) + ' AM'

    elif hour > 12:
        if minute < 10:
            return label + str(hour-12) + ':' + '0' + str(minute) + ' PM'
        else:
            return label + str(hour-12) + ':' + str(minute) + ' PM'

def listoftimes():
    hours = [4+12, 5+12, 6+12, 7+12, 8+12, 9+12, 10+12, 11+12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1+12, 2+12, 3+12]
    minutes = [0, 15, 30 , 45]
    output = []
    for hour in hours:
        for minute in minutes:
            output.append((time(hour=hour, minute=minute), getLabel(minute, hour)))
    return output

def main():
    print(listoftimes())
    

if __name__ == "__main__":
    main()