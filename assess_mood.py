import pandas as pd
import matplotlib.pyplot as plt
import datetime

mood_df = pd.read_csv('Daylio_CSV_Export_200228.csv')

# Function to convert moods to numbers
def numerical_mood(mood):
    if mood == 'great':
        return 5
    elif mood == 'good':
        return 4
    elif mood == 'grand':
        return 3
    elif mood == 'bad':
        return 2
    elif mood == 'shite':
        return 1
# Function to replace separator in activities list
def remove_it(activities):
    return str(activities).replace(" | ", ",").split(",")
# Function to reduce older mood data by one
def normalise(datemood):
    return datemood - 1

# Preprocess data
mood_df = mood_df.drop(["date", "note"] , axis=1)
mood_df["mood"] = mood_df["mood"].map(numerical_mood)
mood_df["activities"] = mood_df["activities"].map(remove_it)
mood_df["caldate"] = mood_df["full_date"]
mood_df["datetime"] = mood_df["full_date"] + " " + mood_df["time"]
mood_df["caldate"] = mood_df["caldate"].apply(pd.to_datetime)
mood_df["datetime"] = mood_df["datetime"].apply(pd.to_datetime)
mood_df = mood_df.drop(["time"] , axis=1)
# Change data values pre-Dec 2019 when mood scores were changed
mood_df.loc[(mood_df['caldate'] < datetime.datetime(2019, 12, 1))\
            & (mood_df['mood'] > 1), ['mood']] = \
mood_df.loc[(mood_df['caldate'] < datetime.datetime(2019, 12, 1))\
            & (mood_df['mood'] > 1), ['mood']].apply(normalise)

# Create new data frame with daily average mood
mood_df['AvgforDay'] = mood_df.groupby('caldate')['mood'].transform('mean')
dailyavg_df = mood_df[['caldate', 'AvgforDay', 'weekday']].drop_duplicates().copy()
dailyavg_df['rollingavg'] = dailyavg_df['AvgforDay'].rolling(30).mean()
dailyavg_df['AvgforWeekday'] = dailyavg_df.groupby('weekday')['AvgforDay'].transform('mean')
dailyavg_df['NormWeekdayAvg'] = dailyavg_df['AvgforWeekday'] - dailyavg_df['AvgforWeekday'].mean()

# Create new data frame for average by days of the week
cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
days = dailyavg_df[['weekday', 'NormWeekdayAvg']].drop_duplicates().copy()
days['weekday'] = pd.Categorical(days['weekday'], categories=cats, ordered=True)
days = days.sort_values('weekday')

# Create list of activities and column for each one
col_act = mood_df['activities'].tolist()
activity_list = []
for sublist in col_act:
    for activity in sublist:
        activity_list.append(activity)
activity_list = list(set(activity_list))
for activity in activity_list:
    mask = mood_df.activities.apply(lambda x: activity in x)
    mood_df.loc[mask == True, activity] = 1

# Present data
plot_pick = input("""What would you like to do? (Only enter letter):\n
a) See mood over time\n
b) See average mood by day of the week\n
c) See average mood for activities\n
d) Output moods in boolean columns to csv\n""")

if plot_pick == 'a':
    # Mood over time
    dailyavg_df.loc[dailyavg_df['caldate'] > datetime.datetime(2018,10,1), ['caldate', 'rollingavg']].plot(kind='line', x='caldate', y='rollingavg', title='Mood over Time')
    plt.show()
elif plot_pick == 'b':
    # Mood by day of the week
    days.plot(kind='bar', x='weekday', y='NormWeekdayAvg', title='Avg by Day')
    plt.show()
elif plot_pick == 'c':
    # Highest scoring activities
    # Filter out columns without enough data
    cut_off = input("""Remove moods with less than __ occurences (Int):\n""")
    mood_filtered = mood_df[mood_df.columns[mood_df.notnull().sum() > int(cut_off)]]
    mood_filtered.iloc[:, 7:] = mood_filtered.iloc[:, 7:].multiply(mood_filtered['mood'], axis="index")
    print(mood_filtered.iloc[:,7:].mean(axis=0).sort_values(ascending=False))
elif plot_pick == 'd':
    # Filter out columns without enough data
    cut_off = input("""Remove moods with less than __ occurences (Int):\n""")
    mood_filtered = mood_df[mood_df.columns[mood_df.notnull().sum() > int(cut_off)]]
    mood_filtered = mood_filtered.fillna(0)
    mood_filtered = mood_filtered.drop(['full_date', 'weekday', 'activities', 'caldate', 'datetime', 'AvgforDay'] , axis=1)
    mood_filtered['mood'] = 0.2*mood_filtered['mood']
    mood_filtered.to_csv(r'boolean_moods.csv', index=False)