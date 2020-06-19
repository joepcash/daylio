def rolling_avg(no_of_days_to_roll=30):
    import pandas as pd
    mood_df = pd.read_csv(r'../../data/interim/gut_scores.csv')

    # Create new data frame with daily average mood
    mood_df['AvgforDay'] = mood_df.groupby('date')['mood'].transform('mean')
    dailyavg_df = mood_df[['date', 'AvgforDay', 'weekday']].drop_duplicates().copy()
    dailyavg_df['rollingavg'] = dailyavg_df['AvgforDay'].rolling(no_of_days_to_roll).mean()

    dailyavg_df.to_csv(r'../../data/interim/moods_rolling_avg.csv', index=False)


def mood_by_weekday():
    import pandas as pd
    dailyavg_df = pd.read_csv(r'../../data/interim/moods_rolling_avg.csv')

    # Create new data frame for average by days of the week
    dailyavg_df['AvgforWeekday'] = dailyavg_df.groupby('weekday')['AvgforDay'].transform('mean')
    dailyavg_df['NormWeekdayAvg'] = dailyavg_df['AvgforWeekday'] - dailyavg_df['AvgforWeekday'].mean()
    cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    days = dailyavg_df[['weekday', 'NormWeekdayAvg']].drop_duplicates().copy()
    days['weekday'] = pd.Categorical(days['weekday'], categories=cats, ordered=True)
    days = days.sort_values('weekday')

    days.to_csv(r'../../data/processed/moods_by_weekday.csv', index=False)

def activity_occurrences():
    import pandas as pd
    import ast
    mood_df = pd.read_csv(r'../../data/interim/gut_scores.csv')

    # Create list of activities and column for each one
    col_act = mood_df['activities'].tolist()
    activity_list = []
    for sublist in col_act:
        for activity in ast.literal_eval(sublist):
            activity_list.append(activity)
    activity_list = list(set(activity_list))
    for activity in activity_list:
        mask = mood_df.activities.apply(lambda x: activity in x)
        mood_df.loc[mask == True, activity] = 1

    mood_df.to_csv(r'../../data/interim/activity_occurrences.csv', index=False)

if __name__ == "__main__":
    rolling_avg(30)
    mood_by_weekday()
    activity_occurrences()