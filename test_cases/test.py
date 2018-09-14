from spirit import state, simulation, constants, geometry, system, hamiltonian, configuration
import numpy as np

class Test:
    name = "base_test_name"
    inputfile = ""
    mu_0 = 2.01335452495e-28
    mu_B = 0.0578838177025
    ddi_mult = - mu_0 * mu_B**2 / (4 * np.pi * 1e-30) 

    def test_energy(self, p_state):
        nos = system.get_nos(p_state)
        pos = np.array(geometry.get_positions(p_state)).reshape(nos, 3)
        spins = np.array(system.get_spin_directions(p_state)).reshape(nos, 3)

        E_BF = self.E_DDI_BF(pos, spins)
        E_Spirit = system.get_energy(p_state)

        return E_BF, E_Spirit

    def test_gradient(self, p_state):
        nos = system.get_nos(p_state)
        pos = np.array(geometry.get_positions(p_state)).reshape(nos, 3)
        spins = np.array(system.get_spin_directions(p_state)).reshape(nos, 3)

        Gradient_BF = self.Gradient_DDI_BF(pos, spins)
        Gradient_Spirit = np.array(system.get_effective_field(p_state)).reshape(nos, 3)

        return Gradient_BF, Gradient_Spirit

    def E_DDI_BF(self, pos, spins, mu_s = 1):
        E = 0
        for i in range(len(pos)):
            for j in range(i+1, len(pos)):
                r = pos[i] - pos[j]
                d = np.linalg.norm(r)
                r /= d
                # E += mult/d**3 * mu[i] * mu[j] * ( 3 * np.dot(spins[i], r) * np.dot(spins[j], r) - np.dot(spins[i], spins[j]) )
                E += self.ddi_mult/d**3 * mu_s**2 * ( 3 * np.dot(spins[i], r) * np.dot(spins[j], r) - np.dot(spins[i], spins[j]) )
        return E

    def Gradient_DDI_BF(self, pos, spins, mu_s = 1):
        gradient = np.zeros(len(pos) * 3).reshape(len(pos), 3)
        for i in range(len(pos)):
            for j in range(len(pos)):
                if i==j:
                    continue
                r = pos[i] - pos[j]
                d = np.linalg.norm(r)
                r /= d
                gradient[i] += self.ddi_mult/d**3 * mu_s * (3 * r * np.dot(spins[j], r) - spins[j])
        return gradient

    def run(self) -> bool:
        print("NOT IMPLEMENTED")
        return True
