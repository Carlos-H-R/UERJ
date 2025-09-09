from math import inf
from PiGenerator import PiGenerator


class Nilakantha(PiGenerator):
    evolution = []

    def generate(self):
        # execute iteration
        mean_error = inf
        iteration = 0
        pi = 0
        i = 2

        while mean_error > self.tol and iteration < self.max_iter:
            pi += 1 / ((i)*(i+1)*(i+2))
            partial_pi = 3 + (4*pi)

            self.evolution.append(partial_pi)
            mean_error = self.mean_error(partial_pi)

            iteration += 1
            i += 2

        pi = 3 + (4 * pi)
        print(f"Realizadas {iteration} iteracoes")
        return round(pi, self.truncate)
    
    def plot_aproximation(self):
        pass


if __name__ == "__main__":
    generator = Nilakantha(6, 1000000, 1e-6)
    pi = generator.generate()

    print(pi)
