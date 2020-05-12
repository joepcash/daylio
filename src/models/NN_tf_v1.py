import tensorflow as tf
import pandas as pd

df = pd.read_csv(r'../../data/interim/mood_features.csv')
activities = list(df.iloc[:,1:].columns.values)

X = df.loc[:,'small meal':].values
target = df.pop('mood')
dataset = tf.data.Dataset.from_tensor_slices((df.values, target.values))
all_dataset = dataset.shuffle(len(df)).batch(1)
test_dataset = all_dataset.take(500)
train_dataset = all_dataset.skip(500)

def get_compiled_model():
    model = tf.keras.Sequential([
    tf.keras.layers.Dense(4, activation='sigmoid'),
    tf.keras.layers.Dense(10, activation='sigmoid'),
    tf.keras.layers.Dense(1, activation='sigmoid')])

    model.compile(optimizer='adam',
                loss='mean_squared_error',
                metrics=['mean_squared_error'])
    return model

model = get_compiled_model()
model.fit(train_dataset, epochs=2)

test_loss, test_acc = model.evaluate(test_dataset, verbose=2)

import eli5
from eli5.sklearn import PermutationImportance

perm = PermutationImportance(model, random_state=1, scoring="neg_mean_squared_error").fit(X, target.values)
print(eli5.explain_weights(perm, activities))