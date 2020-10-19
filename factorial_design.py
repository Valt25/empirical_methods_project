from typing import List, Tuple

import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
import scipy.stats

ACTIVITY_PATH = 'data/ACTIVITY/ACTIVITY_1599420001167.csv'
HEARTRATE_PATH = 'HEARTRATE_MEAN.csv'  # Got from compute_mean_heartrate_per_day.py
SLEEP_PATH = 'data/SLEEP/SLEEP_1599420002569.csv'

ACTIVITY_NAME = 'steps'
HEARTRATE_NAME = 'heartRate'
SLEEP_NAME = 'sleep'


def get_date_triplets():
    sleep_dict = {}
    sleep_df = pd.read_csv(SLEEP_PATH)
    for _, sleep in sleep_df.iterrows():
        sleep_dict[sleep['date']] = sleep['deepSleepTime'] + sleep['shallowSleepTime']

    heartrate_dict = {}
    heartrate_df = pd.read_csv(HEARTRATE_PATH)
    for _, heartrate in heartrate_df.iterrows():
        heartrate_dict[heartrate['date']] = heartrate['heartRate']

    steps_dict = {}
    steps_df = pd.read_csv(ACTIVITY_PATH)
    for _, step in steps_df.iterrows():
        steps_dict[step['date']] = step['steps']

    data = []
    for key in heartrate_dict:
        data.append([heartrate_dict[key], steps_dict[key], sleep_dict[key]])

    combined_df = pd.DataFrame(data, columns=['heartRate', 'steps', 'sleep'])
    return combined_df


def get_linear_regression_line_from_data(data: pd.DataFrame, independent: str, dependent: str) -> pd.DataFrame:
    regression = linear_model.LinearRegression()
    independent_array = data[independent].to_numpy().reshape(-1, 1)
    regression.fit(independent_array, data[dependent])
    return pd.DataFrame({independent: data[independent],
                         dependent: regression.predict(independent_array)})


def find_correlation(data: pd.DataFrame, source: str, dest: str) -> Tuple[float, float]:
    return scipy.stats.pearsonr(data[source], data[dest])


def delete_outliers(combined_df: pd.DataFrame) -> pd.DataFrame:
    return combined_df[combined_df['sleep'] > 0]


combined_data = get_date_triplets()
combined_data = delete_outliers(combined_data)
combined_data = combined_data[(combined_data['sleep'] < combined_data.quantile(.99)['sleep']) & (combined_data['sleep'] > combined_data.quantile(.01)['sleep'])]
combined_data = combined_data[(combined_data['steps'] < combined_data.quantile(.99)['steps']) & (combined_data['steps'] > combined_data.quantile(.01)['steps'])]
combined_data = combined_data[(combined_data['heartRate'] < combined_data.quantile(.99)['heartRate']) & (combined_data['heartRate'] > combined_data.quantile(.01)['heartRate'])]

combined_data = combined_data.sort_values(by=['steps'])

sleep_pertentiles = [
    combined_data.quantile(.25)['sleep'],
    combined_data.quantile(.50)['sleep'],
    combined_data.quantile(.75)['sleep']
]
first_sleep_group = combined_data[combined_data['sleep'] < sleep_pertentiles[0]]

second_sleep_group = combined_data[
    (combined_data['sleep'] < sleep_pertentiles[1]) & (combined_data['sleep'] > sleep_pertentiles[0])]

third_sleep_group = combined_data[
    (combined_data['sleep'] < sleep_pertentiles[2]) & (combined_data['sleep'] > sleep_pertentiles[1])]

forth_sleep_group = combined_data[combined_data['sleep'] > sleep_pertentiles[2]]

print('all data', 'correlation: %.10f, p-value: %.10f' % find_correlation(combined_data, 'steps', 'heartRate'))
print('0-25:', 'correlation: %.10f, p-value: %.10f' % find_correlation(first_sleep_group, 'steps', 'heartRate'))
print('25-50:', 'correlation: %.10f, p-value: %.10f' % find_correlation(second_sleep_group, 'steps', 'heartRate'))
print('50-75:', 'correlation: %.10f, p-value: %.10f' % find_correlation(third_sleep_group, 'steps', 'heartRate'))
print('75-100:', 'correlation: %.10f, p-value: %.10f' % find_correlation(forth_sleep_group, 'steps', 'heartRate'))

plt.plot('steps', 'heartRate', data=get_linear_regression_line_from_data(combined_data, 'steps', 'heartRate'), color='black', label='all data')
plt.plot('steps', 'heartRate', data=get_linear_regression_line_from_data(first_sleep_group, 'steps', 'heartRate'), color='red',
         label='0-25 percentile of sleep')
plt.plot('steps', 'heartRate', data=get_linear_regression_line_from_data(second_sleep_group, 'steps', 'heartRate'), color='blue',
         label='25-50 percentile of sleep')
plt.plot('steps', 'heartRate', data=get_linear_regression_line_from_data(third_sleep_group, 'steps', 'heartRate'), color='green',
         label='50-75 percentile of sleep')
plt.plot('steps', 'heartRate', data=get_linear_regression_line_from_data(forth_sleep_group, 'steps', 'heartRate'), color='yellow',
         label='75-100 percentile of sleep')

plt.xlabel('Steps per day')
plt.ylabel('Mean heart rate per day')

plt.legend()
plt.show()
