import pandas as pd
import tabulate as tabulate
import numpy as np

df = pd.read_csv(r'../../data/interim/activity_occurrences.csv')

df = df.fillna(0)
df.iloc[:,5:] = df.iloc[:,5:].astype(bool)
df['datetime'] = pd.to_datetime(df['datetime'])
df['index'] = df['datetime']
df = df.set_index('index')
df = df.between_time('08:00', '00:00')
df['rank'] = df.groupby(df['datetime'].dt.date)['datetime'].rank(ascending=True)
df['datetime'] = np.where(df['rank'] == 1,
                         df['datetime'] -
                         (df['datetime'] -
                          (pd.to_datetime(df['date']) + pd.Timedelta(hours=8)))/2
                         , df['datetime'] - (df['datetime'].diff(periods=-1))/2)
df.drop(columns=['date','rank','activities','weekday'], axis=1, inplace=True)
df.reset_index()
print(df.info())

df.to_csv(r'../../data/processed/time_since_activity_features.csv', index=False)