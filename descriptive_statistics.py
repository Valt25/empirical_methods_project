import pandas as pd
import matplotlib.pyplot as plt

ACTIVITY_PATH = 'data/ACTIVITY/ACTIVITY_1599420001167.csv'
HEARTRATE_PATH = 'data/HEARTRATE_AUTO/HEARTRATE_AUTO_1599420004856.csv'
SLEEP_PATH = 'data/SLEEP/SLEEP_1599420002569.csv'

ACTIVITY_NAME = 'steps'
HEARTRATE_NAME = 'heartRate'
SLEEP_NAME = 'sleep'

## Put here the right variable to see different results
VARIABLE_NAME = SLEEP_NAME
FILE_PATH = SLEEP_PATH

data = pd.read_csv(FILE_PATH)

if VARIABLE_NAME == 'sleep':
    def mapRow(row):
        print(row)
        return row['shallowSleepTime'] + row['deepSleepTime']
    data['sleep'] = data['shallowSleepTime'] + data['deepSleepTime']

mean = data.mean()[VARIABLE_NAME]
std = data.std()[VARIABLE_NAME]
print('mean', mean)
print('standard deviation', std)

ax = data[VARIABLE_NAME].plot.density()

ax.plot()
plt.axvline(x=mean, color='red')
plt.axvline(x=mean+std, color='green')
plt.axvline(x=mean-std, color='green')

plt.show()
