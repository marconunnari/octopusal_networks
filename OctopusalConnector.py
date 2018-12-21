import numpy as np

class OctopusalConnector():
    
    def __init__(self, input_size, output_size):
        self.connectedness = np.zeros((input_size, output_size))
        
    def train(self, input, output):
        self.connectedness += np.outer(input, output)
    
    def predict(self, input):
        input = input.reshape((-1, 1))
        connectedness_output = self.connectedness * input    
        output = connectedness_output.sum(axis=0)
        return output
