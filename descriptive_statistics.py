import pandas as pd

ACTIVITY_PATH = 'data/ACTIVITY/ACTIVITY_1599420001167.csv'
HEARTRATE_PATH = 'data/HEARTRATE_AUTO/HEARTRATE_AUTO_1599420004856.csv'
SLEEP_PATH = 'data/SLEEP/SLEEP_1599420002569.csv'

ACTIVITY_NAME = 'steps'
HEARTRATE_NAME = 'heartRate'
SLEEP_NAME = 'sleep'

VARIABLE_NAME = SLEEP_NAME
FILE_PATH = SLEEP_PATH

data = pd.read_csv(FILE_PATH)

if VARIABLE_NAME == 'sleep':
    def mapRow(row):
        print(row)
        return row['shallowSleepTime'] + row['deepSleepTime']
    data['sleep'] = data['shallowSleepTime'] + data['deepSleepTime']

print(data.mean()[VARIABLE_NAME])
print(data.std()[VARIABLE_NAME])
