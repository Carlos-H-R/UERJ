from math import inf
from PiGenerator import PiGenerator


class BBP(PiGenerator):
    evolution = []

    def generate(self):
        # execute iteration
        iteration = 0
        pi = 0
        mean_error = inf

        while mean_error > self.tol and iteration < self.max_iter:
            coef = 1/(16**iteration)
            factor = (8*iteration)+1
            pi += coef*((4/factor)-(2/(factor+3))-(1/(factor+4))-(1/(factor+5)))

            mean_error = self.mean_error(pi)
            self.evolution.append(pi)

            iteration += 1

        print(f"Realizadas {iteration} iteracoes")
        return round(pi, self.truncate)
    
    def plot_aproximation(self):
        pass


if __name__ == "__main__":
    generator = BBP(6, 10000, 1e-9)
    pi = generator.generate()

    print(pi)
