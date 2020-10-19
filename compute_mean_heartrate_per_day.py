from collections import Counter

import pandas as pd

HEARTRATE_PATH = 'data/HEARTRATE_AUTO/HEARTRATE_AUTO_1599420004856.csv'

data = pd.read_csv(HEARTRATE_PATH)

heartrate_sum_per_day = Counter()
heartrate_measures_per_day = Counter()

for _, measurement in data.iterrows():
    heartrate_measures_per_day[measurement['date']] += 1
    heartrate_sum_per_day[measurement['date']] += measurement['heartRate']

dates = []
heart_rates = []
for date in heartrate_sum_per_day.keys():
    dates.append(date)
    heart_rates.append(int(heartrate_sum_per_day[date] / heartrate_measures_per_day[date]))


new_df = pd.DataFrame({'date': dates, 'heartRate': heart_rates})
new_df.to_csv('HEARTRATE_MEAN.csv', index=False)
