import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv(r'../../data/interim/mood_features.csv')
activities = list(df.iloc[:, 1:].columns.values)
dataset = df.copy()

train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

train_labels = train_dataset.pop('mood')
test_labels = test_dataset.pop('mood')

estimator = tf.estimator.LinearRegressor(feature_columns=train_dataset)

bob = pd.DataFrame({k: train_dataset[k].values for k in activities})
print(bob.head())

def get_input_fn(num_epochs=None, n_batch=200, shuffle=True):
    return tf.compat.v1.estimator.inputs.pandas_input_fn(
        x=pd.DataFrame({k: train_dataset[k].values for k in activities}),
        y=pd.Series(train_labels.values),
        batch_size=n_batch,
        num_epochs=num_epochs,
        shuffle=shuffle)


estimator.train(input_fn=get_input_fn(num_epochs=None, n_batch=128, shuffle=True), steps=1000)
