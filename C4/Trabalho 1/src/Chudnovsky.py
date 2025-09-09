from math import inf, sqrt, factorial
from PiGenerator import PiGenerator

class Chudnovsky(PiGenerator):
    evolution = []
    fact_memory = [1,1,1,2]

    def generate(self):
        # execute iteration
        mean_error = inf
        iteration = 0
        pi = 0 # = mp.mpf(0)

        C = 426880 * sqrt(10005)

        M = 13591409
        L = 545140134
        X = mp.mpf(-262537412640768000)

        while mean_error > self.tol and iteration < self.max_iter:
            k6 = factorial(6*iteration)
            k3 = factorial(3*iteration)
            k = factorial(iteration)

            nume = k6 * (M + L * iteration)
            deno = k3 * (k**3) * (X**k)

            pi += nume / deno

            partial_pi = C / pi

            mean_error = self.mean_error(partial_pi)
            self.evolution.append(partial_pi)

            iteration += 1

        pi = C / pi
        print(f"Realizadas {iteration} iteracoes")
        return pi
    
    def plot_aproximation(self):
        pass


if __name__ == "__main__":
    generator = Chudnovsky(5, 1000, 1e-6)
    pi = generator.generate()

    print(pi)
    