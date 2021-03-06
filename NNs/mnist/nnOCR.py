import numpy as np
import random
import datetime
import json


class nnOCR(object):

    def __init__(self, learn_rate=3.0, layers=[784, 16, 16, 10], model=None, dropout=None):
        self.num_layers = len(layers)
        self.layers = layers
        if model is None:
            self.biases = [np.random.randn(y, 1) for y in layers[1:]]
            self.weights = [np.random.randn(y, x) for x, y in zip(layers[:-1], layers[1:])]
        else:
            self.weights, self.biases = self.load_model(model)
        self.dropout = dropout
        self.mapper = np.vectorize(self.sigmoid)
        self.learn_rate = np.array([learn_rate])

    def sigmoid(self, z):
        return 1.0 / (1.0 + np.exp(-z))

    def sigmoid_der(self, z):
        return self.sigmoid(z) * (1 - self.sigmoid(z))

    @staticmethod
    def ReLU(z):
        if z > 0:
            return z
        else:
            return 0

    @staticmethod
    def ReLU_der(z):
        if z > 0:
            return 1
        else:
            return 0

    def classify(self, v):
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, v) + b
            v = self.mapper(z)
        return self.softmax(z).flatten() #return v.flatten()

    @staticmethod
    def softmax(inputs):
        in_sum = np.sum(np.exp(inputs))
        return np.exp(inputs) / in_sum

    def backward(self, inputs, predict):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        v = inputs
        vs = [inputs]  # list to store all the activations, layer by layer
        zs = []  # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, v) + b
            zs.append(z)
            v = self.mapper(z)
            vs.append(v)
        vs[-1] = self.softmax(z)
        if self.dropout is not None:
            mask = [(np.random.rand(*v.shape) < self.dropout) / 1 for v in vs]
            mask[-1] = np.ones(mask[-1].shape)
            vs = [v*m for v, m in zip(vs, mask)]
        # backward pass
        e = self.final_error(vs[-1], predict)
        g = e

        for i in reversed(range(self.num_layers - 1)):
            nabla_b[i] = g
            nabla_w[i] = g.dot(vs[i].transpose())
            sig = self.sigmoid_der(zs[i - 1])
            e = np.dot(np.transpose(self.weights[i]), g)
            if i > 0:
                g = sig * e
        return nabla_b, nabla_w

    @staticmethod
    def final_error(output_activations, y):
        return output_activations - y

    def update_backward(self, batch, learn_rate):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for inputs, predict in batch:
            delta_nabla_b, delta_nabla_w = self.backward(inputs, predict)
            for i in range(len(nabla_b)):
                nabla_b[i] += delta_nabla_b[i]
            for i in range(len(nabla_w)):
                nabla_w[i] += delta_nabla_w[i]
        for i in range(len(self.weights)):
            self.weights[i] -= (learn_rate / len(batch)) * nabla_w[i]
        for i in range(len(self.biases)):
            self.biases[i] -= (learn_rate / len(batch)) * nabla_b[i]

    def train(self, training_data, epochs, batch_size, test_data=None):
        if test_data:
            n_test = len(test_data)
        n = len(training_data)
        for j in range(epochs):
            t0 = datetime.datetime.now().timestamp()
            random.shuffle(training_data)
            mini_batches = [training_data[k:k + batch_size] for k in range(0, n, batch_size)]
            for mini_batch in mini_batches:
                self.update_backward(mini_batch, self.learn_rate)
            if test_data:
                eval = self.evaluate(test_data)
                t0 = datetime.datetime.now().timestamp() - t0
                print("Epoch {0} ({4:.5} s): {1} out of {2} correct ({3:.2%})".format(j, eval, n_test, eval/n_test, t0))
            else:
                print("Epoch {0} complete".format(j))

    def evaluate(self, test_data):
        test_results = [(np.argmax(self.classify(x)), (np.argmax(y))) for x, y in test_data]
        r = 0
        for x, y in test_results:
            if x == y:
                r += 1
        return r

    def load_model(self, path):
        with open(path) as infile:
            data = json.load(infile)
        return [np.array(x) for x in data['weights']], [np.array(x) for x in data['biases']]

    def save_model(self, path):
        d = dict(weights=[x.tolist() for x in self.weights], biases=[x.tolist() for x in self.biases])
        with open(path, 'w') as outfile:
            json.dump(d, outfile)
