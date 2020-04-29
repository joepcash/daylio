# Cleans raw mood data as provided by Daylio
# mood_change_fix only exists due to a change in how
# I scored my mood starting from December 2019.
# Simply set it to false if you're not me.
def clean_moods(mood_change_fix = False):
    import pandas as pd
    import datetime

    mood_df = pd.read_csv('../../data/raw/Daylio_CSV_Export_200228.csv')

    # Drop unneeded columns
    mood_df = mood_df.drop(["date", "note"] , axis=1)
    # Convert moods to numerical scale
    mood_df["mood"] = mood_df["mood"].map(numerical_mood)
    # Remove separator between activities
    mood_df["activities"] = mood_df["activities"].map(remove_separator)
    # Create columns for date and datetime
    mood_df["datetime"] = mood_df["full_date"] + " " + mood_df["time"]
    mood_df["datetime"] = mood_df["datetime"].apply(pd.to_datetime)
    mood_df["date"] = mood_df["full_date"].apply(pd.to_datetime)
    # Remove no longer needed time column
    mood_df = mood_df.drop(["time", "full_date"] , axis=1)

    # Fix for mood data pre-Dec 2019 as in December, the way moods were
    # scored was changed
    if mood_change_fix == True:
        mood_df.loc[(mood_df['date'] < datetime.datetime(2019, 12, 1))\
                    & (mood_df['mood'] > 1), ['mood']] = \
        mood_df.loc[(mood_df['date'] < datetime.datetime(2019, 12, 1))\
                    & (mood_df['mood'] > 1), ['mood']].apply(normalise)

    mood_df.to_csv(r'../../data/interim/moods_clean.csv', index=False)
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
def remove_separator(activities):
    return str(activities).replace(" | ", ",").split(",")
# Function to reduce older mood data by one
def normalise(datemood):
    return datemood - 1

if __name__ == "__main__":
    clean_moods(True)