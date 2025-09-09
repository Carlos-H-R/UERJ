from math import inf

import numpy as np
from PiGenerator import PiGenerator


class Machin(PiGenerator):
    def generate(self):
        # execute iteration
        pi = 0
        mean_error = inf

        pi = (4 * (np.arctan(1/5))) - (np.arctan(1/239))
        pi = 4 * pi

        return pi
    

if __name__ == "__main__":
    generator = Machin(6, 10000, 1e-6)
    pi = generator.generate()

    print(pi)
