import numpy as np

class Test:
    name = "base_test_name"
    inputfile = ""
    mu_0 = 2.01335452495e-28
    mu_B = 0.0578838177025

    def E_DDI_BF(self, pos, spins, mu_s = 1):
        E = 0
        mult = - self.mu_0 * self.mu_B**2 / (4 * np.pi * 1e-30) 
        for i in range(len(pos)):
            for j in range(i+1, len(pos)):
                r = pos[i] - pos[j]
                d = np.linalg.norm(r)
                r /= d
                # E += mult/d**3 * mu[i] * mu[j] * ( 3 * np.dot(spins[i], r) * np.dot(spins[j], r) - np.dot(spins[i], spins[j]) )
                E += mult/d**3 * mu_s**2 * ( 3 * np.dot(spins[i], r) * np.dot(spins[j], r) - np.dot(spins[i], spins[j]) )
        return E

    def Gradient_DDI_BF(self, pos, spins, mu_s = 1):
        return 0

    def run(self) -> bool:
        print("NOT IMPLEMENTED")
        return True



