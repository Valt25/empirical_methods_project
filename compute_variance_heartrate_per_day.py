from collections import Counter

import pandas as pd


def pop_std(x):
    return x.std(ddof=0)

HEARTRATE_PATH = 'data/HEARTRATE_AUTO/HEARTRATE_AUTO_1599420004856.csv'

data = pd.read_csv(HEARTRATE_PATH)
print(data)
data = data.groupby('date').agg('std')
print(data)
data.to_csv('HEARTRATE_VARIANCE.csv')
