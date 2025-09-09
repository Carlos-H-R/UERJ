import numpy as np


class PiGenerator():
    xPI: np.double = 0
    
    def __init__(self, truncate: int, max_iter: int, tol: float):
        self.truncate = truncate
        self.max_iter = max_iter
        self.tol = tol

    def set_precision(self, precision):
        self.pi_precision = precision

    def set_truncate(self, truncate):
        self.truncate = truncate

    def set_tol(self, tol):
        # Set a new 
        self.tol = tol

    def mean_error(self, value):
        m_error = (np.pi - value) ** 2
        return m_error
        
    def show(self):
        print(self.xPI.round(self.pi_precision))
