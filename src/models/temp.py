import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r'../../data/interim/mood_features.csv')
activities = list(df.iloc[:, 1:].columns.values)
dataset = df.copy()

train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

train_labels = train_dataset.pop('mood')
test_labels = test_dataset.pop('mood')

# Define layer
layer0 = tf.keras.layers.Dense(units=1, input_shape=[52])
model = tf.keras.Sequential([layer0])

# Compile model
model.compile(loss='mean_squared_error',
              optimizer=tf.keras.optimizers.Adam(0.01))

# Train the model
history = model.fit(train_dataset, train_labels, epochs=20, verbose=False)

plt.xlabel('Epoch Number')
plt.ylabel("Loss Magnitude")
plt.plot(history.history['loss'])
plt.show()

# Prediction
mse = 0
predictions = model.predict(test_dataset)
tests = test_labels.values
for i in range(len(tests)):
    mse += (tests[i] - predictions[i])**2
mse /= len(test_labels)
print(mse)

# Get weight and bias
weights = layer0.get_weights()
#for i in range(len(activities)):
#    print('weight: {} activity: {}'.format(weights[0][i], activities[i]))
w = []
for i in range(len(weights[0])):
    w.append(weights[0][i][0])
activity_weights = pd.DataFrame({'Activity': activities, 'Weight': w},
                                columns = ['Activity', 'Weight'])

activity_weights.to_csv(r'../../data/processed/lr_weights.csv', index=False)