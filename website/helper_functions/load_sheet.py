import os
import pandas as pd
import datetime as dt
import time as t

from flask import current_app
from .. import db

from .exc import SpreadSheetParseError

from ..models.campaigns import Campaigns
from ..models.users import Users
from ..models.shiftstamps import Activities, ShiftStamps

import_start = 0
import_end = 0
process_start = 0
process_end = 0

def main():
    filename = 'import_saihaan_payments_2022-04-16.xlsx'
    import_type = 'Shifts'
    prod_start(filename, import_type)

if __name__ == '__main__':
    
    main()

def load_sheet_as_df(filename, sheet) -> pd.DataFrame:

    filenameSplit, filename_extension = os.path.splitext(filename)
    if filename_extension == '.csv':
        df =  pd.read_csv(filename, sheet, engine='python', index=False)
    else:
        df = pd.read_excel(filename, sheet)
    return df

def test_start(filename, import_type):
    df = load_sheet_as_df('paymentWebApp\\uploads\\imports\\import_saihaan_payments_2022-04-16.xlsx', 'Shifts')
    process_spreadsheet(df, import_type)

def prod_start(filename, import_type):
    global import_start 
    global import_end
    global process_start
    global process_end
    import_start = t.perf_counter()
    path_value = os.path.join(os.path.dirname(current_app.instance_path), current_app.config['IMPORT_FOLDER'], filename)
    df = load_sheet_as_df(path_value, import_type)
    process_start = t.perf_counter()
    process_spreadsheet(df, import_type)
    process_end = t.perf_counter()
    import_end = t.perf_counter()
    import_time = import_end - import_start
    process_time = process_end = process_start
    current_app.logger.info('Import Took: ' + str(import_time))
    current_app.logger.info('Process Took: '+ str(process_time))

def process_spreadsheet(df: pd.DataFrame, import_type):
    if import_type == 'Shifts':
        #Iterate Over Each Line
        df_dict = df.to_dict('records')
        for index, row in df.iterrows():
            user = Users.query.filter_by(alias = row['alias']).first()
            if user:
                #Process Row
                process_row(user, row)
            else:
                db.session.commit()

def process_row(user, row):
    campaign = Campaigns.query.filter_by(alias=row['campaign_alias']).first()
    if campaign:
        comparedShift = ShiftStamps.query.filter_by(user_id=user.id, start_time=process_date_string(row['date'], row['start_time'])).first()
        if comparedShift:
            pass
        else:
            shifstamp = ShiftStamps(
                user_id = user.id,
                start_time = process_date_string(row['date'], row['start_time']),
                end_time = process_date_string(row['date'], row['end_time']),
                minutes = row['minutes'],
                campaign_id = campaign.id,
                activity_id = Activities.query.filter_by(activity=row['activity']).first().activity,
                hourly_rate = row['rate']
            )
            db.session.add(shifstamp)
            db.session.commit()

def process_date_string(date, time):
    dateObj = process_date_part(date)
    timeObj = process_time_part(time)

    return dt.datetime.combine(dateObj, timeObj)

def process_date_part(date):
    if '/' in str(date):
        pieces = str(date).split('/')
        dateObj = dt.date(year=pieces[0], month=pieces[1], day=pieces[2]) 
    elif '-' in str(date):
        pieces = str(date).split('-')
        dateObj = dt.date(year=int(pieces[0]), month=int(pieces[1]), day=int(pieces[2].split()[0])) 

    return dateObj

def process_time_part(time):
    if ':' in str(time):
        pieces = str(time).split(':')

        timeObj = dt.time(hour=int(pieces[0]), minute=int(pieces[1]), second=int(pieces[2].split()[0])) 
    else:
        raise SpreadSheetParseError('time parse error')

    return timeObj


