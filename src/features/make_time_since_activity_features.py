import pandas as pd
import tabulate as tabulate

df = pd.read_csv(r'../../data/interim/activity_occurrences.csv')

df = df.fillna(0)
df.iloc[:,5:] = df.iloc[:,5:].astype(bool)
df['datetime'] = pd.to_datetime(df['datetime'])
df['index'] = df['datetime']
df['time'] = df['datetime'].dt.time
df['date'] = df['datetime'].dt.date
df = df.set_index('index')
df = df.between_time('08:00', '00:00')
df['rank'] = df.groupby('date')['datetime'].rank(ascending=True)
df['diff'] = df['datetime'].diff(periods=-1)
df['newtime'] = df['datetime'] - df['diff']/2
df.loc[df['rank'] == 1, 'newtime'] = pd.Timestamp()

df.to_csv(r'../../data/processed/time_since_activity_features.csv', index='False')