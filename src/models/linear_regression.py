import tensorflow as tf
import pandas as pd

df = pd.read_csv(r'../../data/interim/mood_features.csv')

train = df.sample(frac=0.8,random_state=200)
test = df.drop(train.index)
train_target = train.pop('mood')
test_target = test.pop('mood')

dataset = tf.data.Dataset.from_tensor_slices((train.values, train_target.values))

for feat, targ in dataset.take(5):
    print ('Features: {}, Target: {}'.format(feat, targ))