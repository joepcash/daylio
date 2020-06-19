import pandas as pd
import numpy as np

df = pd.read_csv(r'../../data/interim/gut_scores.csv')

df = df.fillna(0)
df.iloc[:,5:] = df.iloc[:,5:].astype(bool)
df['datetime'] = pd.to_datetime(df['datetime'])
# Create a datetime index which is needed for the later groupby, I think
df['index'] = df['datetime']
df = df.set_index('index')
# Remove entries in the middle of the night as these are unrepresentative
# as well as there being not enough data points in this time frame
df = df.between_time('08:00', '00:00')
# Rank entries in order of occurrence per each day
df['rank'] = df.groupby(df['datetime'].dt.date)['datetime'].rank(ascending=True)
# Set time of each entry as the halfway point between the time of the entry
# and time of the prior one. For the first entry of each day, instead set its
# time as the halfway point between the time of the entry and 8 a.m..
df['datetime'] = np.where(df['rank'] == 1,
                         df['datetime'] -
                         (df['datetime'] -
                          (pd.to_datetime(df['datetime'].dt.date) +
                           pd.Timedelta(hours=8)))/2
                         , df['datetime'] - (df['datetime'].diff(periods=-1))/2)
df.drop(columns=['date','rank','activities','weekday'], axis=1, inplace=True)
df.reset_index()
for i in range(2, len(df.columns)):
    # When an activity occurs, set the activity's value to the entry's datetime.
    df.iloc[:, i] = np.where(df.iloc[:, i] == True,
                             df['datetime'].apply(str),
                             df.iloc[:, i])
    # When an activity does not occur, set the activity's value to the datetime
    # of the most recent entry in which it did occur.
    df.iloc[:, i] = df.iloc[:, i].replace(to_replace=False, method='bfill')
    df.iloc[:, i] = df.iloc[:, i].replace(False, np.NaN)
    # For each activity in each entry, calculate time since activity last occurred.
    df.iloc[:, i] = df['datetime'] - pd.to_datetime(df.iloc[:, i])
    df.iloc[:, i] = df.iloc[:,i] / pd.Timedelta(hours=1)

df.drop('datetime', axis=1, inplace=True)
df.dropna(axis=1, how = 'all', inplace=True)
df.to_csv(r'../../data/processed/time_since_activity_features.csv', index=False)