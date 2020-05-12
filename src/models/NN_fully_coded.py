def neural_network():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # create NeuralNetwork class
    class NeuralNetwork:

        # intialize variables in class
        def __init__(self, inputs, outputs):
            self.inputs  = inputs
            self.outputs = outputs
            # initialize weights as .50 for simplicity
            w_a = []
            for x in inputs[0]:
                w_a.append([.50])
            self.weights = np.array(w_a)
            self.error_history = []
            self.epoch_list = []

        #activation function ==> S(x) = 1/1+e^(-x)
        def sigmoid(self, x, deriv=False):
            if deriv == True:
                return x * (1 - x)
            return 1 / (1 + np.exp(-x))

        # data will flow through the neural network.
        def feed_forward(self):
            self.hidden = self.sigmoid(np.dot(self.inputs, self.weights))

        # going backwards through the network to update weights
        def backpropagation(self):
            self.error  = self.outputs - self.hidden
            delta = self.error * self.sigmoid(self.hidden, deriv=True)
            self.weights += np.dot(self.inputs.T, delta)

        # train the neural net for 25,000 iterations
        def train(self, epochs=300):
            for epoch in range(epochs):
                # flow forward and produce an output
                self.feed_forward()
                # go back though the network to make corrections based on the output
                self.backpropagation()
                # keep track of the error history over each epoch
                self.error_history.append(np.average(np.abs(self.error)))
                self.epoch_list.append(epoch)

        # function to predict output on new and unseen input data
        def predict(self, new_input):
            prediction = self.sigmoid(np.dot(new_input, self.weights))
            return prediction

        def return_weights(self):
            return self.weights

    data = pd.read_csv('data/interim/mood_features.csv')
    x = data.iloc[:,1:].to_numpy()
    pre_y = data.iloc[:,0].to_numpy()
    headers = list(data.iloc[:,1:].columns)
    y = []
    for i in range(len(pre_y)):
        y.append([pre_y[i]])

    # create neural network
    NN = NeuralNetwork(x, y)
    # train neural network
    NN.train()
    final_weights = NN.return_weights()
    results = []
    for i in range(len(final_weights)):
        results.append([headers[i], final_weights[i][0]])

    results_df = pd.DataFrame(data=results)
    print(results_df.sort_values(by=[1],ascending=False))
    results_df.sort_values(by=[1],ascending=False)
    results_df.sort_values(by=[1],ascending=False).to_csv(r'data/processed/NN_results.csv', index=False)
    # plot the error over the entire training duration
    plt.figure(figsize=(15,5))
    plt.plot(NN.epoch_list, NN.error_history)
    plt.xlabel('Epoch')
    plt.ylabel('Error')
    #plt.show()

if __name__ == "__main__":
    neural_network()