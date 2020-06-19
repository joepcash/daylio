def make_gut_score():
    import pandas as pd
    import numpy as np

    mood_df = pd.read_csv('../../data/interim/activity_occurrences.csv')

    mood_df.loc[mood_df['very bad'] == 1, ['bad']] = np.NaN

    mood_df = mood_df[(mood_df['very bad'] == 1) |
                      (mood_df['bad'] == 1) |
                      (mood_df['okay'] == 1) |
                      (mood_df['good'] == 1)]

    mood_df = mood_df.fillna(0)
    mood_df['mood'] = 3*mood_df['good'] + 2*mood_df['okay'] + mood_df['bad']
    mood_df.drop(['very bad', 'bad', 'okay', 'good'], axis = 1, inplace=True)

    mood_df.to_csv(r'../../data/interim/gut_scores.csv', index=False)

if __name__ == "__main__":
    make_gut_score()