def visualise_food_groups():
    import pandas as pd
    import matplotlib.pyplot as plt

    mood_df = pd.read_csv('../../data/processed/time_since_activity_features.csv')

    foods = ['Alcohol','Chilli','Lactose','Fructose','Polyols-sorbitol',
             'Polyols-mannitol','Fructans-wheat','Fructans-onions',
             'Fructans-garlic','Galacto oligo-saccharides']

    cols = foods
    cols.append('mood')

    mood_df = mood_df[cols]
    print(mood_df.info())

    fno = 2
    mood_df[['mood',foods[fno]]].plot.scatter(y='mood',x=foods[fno])

    plt.show()

if __name__ == "__main__":
    visualise_food_groups()