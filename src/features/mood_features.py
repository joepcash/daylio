def mood_features(cut_off):
    import pandas as pd
    mood_df = pd.read_csv(r'../../data/interim/activity_occurrences.csv')

    # Filter out columns without enough data
    mood_filtered = mood_df[mood_df.columns[mood_df.notnull().sum() > int(cut_off)]]
    mood_filtered = mood_filtered.fillna(0)
    mood_filtered = mood_filtered.drop(['weekday', 'activities', 'date', 'datetime'], axis=1)
    mood_filtered['mood'] = 0.2 * mood_filtered['mood']

    mood_filtered.to_csv(r'../../data/interim/mood_features.csv', index=False)

if __name__ == "__main__":
    mood_features(30)