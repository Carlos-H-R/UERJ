from math import factorial, inf

import numpy as np
from PiGenerator import PiGenerator


class Ramanujan(PiGenerator):
    evolution = []
    fact_memory = [1,1,1,2]

    def generate(self):
        # execute iteration
        mean_error = inf
        iteration = 0
        pi = 0


        factor = (2*(2**(1/2)))/9801

        while mean_error > self.tol and iteration < self.max_iter:
            k4 = self.factorial(4*iteration)
            k = self.factorial(iteration)

            pi += (k4 * (1103 + (26390*iteration))) / ((k**4) * (396**(4*iteration)))

            partial_pi = (factor * pi) ** (-1)

            mean_error = self.mean_error(partial_pi)
            self.evolution.append(partial_pi)

            iteration += 1

        pi = (factor * pi) ** (-1)
        print(f"Realizadas {iteration} iteracoes")
        return pi
    
    def factorial(self, n):
        if n < len(self.fact_memory):
            return self.fact_memory[n]
        
        else:
            fact = n * self.factorial(n-1)
            return fact
    
    def plot_aproximation(self):
        pass


if __name__ == "__main__":
    generator = Ramanujan(5, 10000, 1e-6)
    pi = generator.generate()

    print(pi)