from math import inf
from PiGenerator import PiGenerator


class Euler(PiGenerator):
    evolution = []

    def generate(self):
        # execute iteration
        mean_error = inf
        iteration = 0
        pi = 0
        i = 1

        while mean_error > self.tol and iteration < self.max_iter:
            pi += 1/(i ** 2)
            partial_pi = (pi*6) ** (1/2)

            mean_error = self.mean_error(pi)
            self.evolution.append(partial_pi)

            iteration += 1
            i += 1

        pi = (pi*6) ** (1/2)

        print(f"Realizadas {iteration} iteracoes")
        return round(pi, self.truncate)
    
    def plot_aproximation(self):
        pass


if __name__ == "__main__":
    generator = Euler(6, 100000, 1e-6)
    pi = generator.generate()

    print(pi)
    