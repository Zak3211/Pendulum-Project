import math
import numpy as np
import random

class NeuralNet:
    def __init__(self,  layers):

        #random architecture
        self.layers = [6]
        for i in range(random.randint(1,10)):
            self.layers.append(random.randint(1,11))
        self.layers.append(1)

        self.weights = []
        self.biases = []

        for i in range(len(layers)-1):
            self.weights.append(np.random.rand(layers[i], layers[i+1]))
            self.biases.append(np.random.rand(layers[i+1], 1))
    
    def normal(self, mu, sigma):
        return int(np.random.normal(mu, sigma))
    
    def ReLU(self, inputs):
        for input in inputs:
            input = max(0,input)
        return inputs
    
    def add_Node(self):
        layer = random.randint(1, len(self.layers)-2)
        node_index = random.randint(0,self.layers[layer])
        
    def forward(self, inputs):
        for i in range(len(self.weights)):
            inputs = np.dot(self.weights[i], inputs) + self.biases[i]
            inputs = self.ReLU(inputs)
        return inputs