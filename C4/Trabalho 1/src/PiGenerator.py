import numpy as np


class PiGenerator():
    xPI: np.double = 0
    
    def __init__(self, pi_precision, truncate, error):
        self.pi_precision = pi_precision
        self.truncate = truncate
        self.error = error

    def set_precision(self, precision):
        self.pi_precision = precision

    def set_truncate(self, truncate):
        self.truncate = truncate

    def set_error(self, error):
        # Set a new 
        self.error = error
        
    def show(self):
        print(self.xPI.round(self.pi_precision))
