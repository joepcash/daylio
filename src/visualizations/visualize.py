def visualize():
    import pandas as pd
    import matplotlib.pyplot as plt
    import datetime

    # Present data
    plot_pick = input("""What would you like to do? (Only enter letter):\n
    a) See mood over time\n
    b) See average mood by day of the week\n
    c) See average mood for activities\n""")

    if plot_pick == 'a':
        dailyavg_df = pd.read_csv(r'../../data/processed/moods_rolling_avg.csv')
        # Mood over time
        dailyavg_df.loc[dailyavg_df['date'].apply(pd.to_datetime) > datetime.datetime(2018,10,1), ['date', 'rollingavg']].plot(kind='line', x='date', y='rollingavg', title='Mood over Time')
        plt.show()
    elif plot_pick == 'b':
        days = pd.read_csv(r'../../data/processed/moods_by_weekday.csv')
        # Mood by day of the week
        days.plot(kind='bar', x='weekday', y='NormWeekdayAvg', title='Avg by Day')
        plt.show()
    elif plot_pick == 'c':
        mood_df = pd.read_csv(r'../../data/interim/activity_occurrences.csv')
        # Highest scoring activities
        # Filter out columns without enough data
        cut_off = input("""Remove moods with less than __ occurences (Int):\n""")
        mood_filtered = mood_df[mood_df.columns[mood_df.notnull().sum() > int(cut_off)]]
        mood_filtered.iloc[:, 7:] = mood_filtered.iloc[:, 7:].multiply(mood_filtered['mood'], axis="index")
        print(mood_filtered.iloc[:,7:].mean(axis=0).sort_values(ascending=False))

if __name__ == "__main__":
    visualize()
