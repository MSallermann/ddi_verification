if __name__ == "__main__":
    path_to_spirit_pkg = "/Users/sallermann/Coding/spirit/core/python"
    import sys
    sys.path.append(path_to_spirit_pkg)

from spirit import state
from spirit import simulation
from spirit import constants
from spirit import geometry
from spirit import system
from spirit import hamiltonian
from spirit import configuration
import numpy as np

name = "Comparison to brute force (energy)"
information = "Comparison to Brute Force Calculations of the energy. Note: The Gradient is also shown, but may be different from the Brute Force Gradient because spirit only takes the component orthogonal to the spin."

tolerance = 1e-4

mu_0 = 2.0133545*1e-28
mu_B = 0.057883817555
ddi_mult = - mu_0 * mu_B**2 / (4 * np.pi * 1e-30) 


def E_DDI_BF(pos, spins, mu_s):
    E = 0
    for i in range(len(pos)):
        for j in range(i+1, len(pos)):
            r = pos[i] - pos[j]
            d = np.linalg.norm(r)
            r /= d
            # E += mult/d**3 * mu[i] * mu[j] * ( 3 * np.dot(spins[i], r) * np.dot(spins[j], r) - np.dot(spins[i], spins[j]) )
            E += ddi_mult/d**3 * mu_s[i] * mu_s[j] * ( 3 * np.dot(spins[i], r) * np.dot(spins[j], r) - np.dot(spins[i], spins[j]) )
    return E

def Gradient_DDI_BF(pos, spins, mu_s):
    gradient = np.zeros(len(pos) * 3).reshape(len(pos), 3)
    for i in range(len(pos)):
        for j in range(len(pos)):
            if i==j:
                continue
            r = pos[i] - pos[j]
            d = np.linalg.norm(r)
            r /= d
            gradient[i] += ddi_mult/d**3 * mu_s[j] * (3 * r * np.dot(spins[j], r) - spins[j])
        return gradient

def test_energy(p_state, mu = None):
    
    nos = system.get_nos(p_state)
    pos = np.array(geometry.get_positions(p_state)).reshape(nos, 3)
    spins = np.array(system.get_spin_directions(p_state)).reshape(nos, 3)

    if type(mu) == type(None):
        mu_s = np.ones(len(pos))
    else:
        mu_s = mu

    E_BF = E_DDI_BF(pos, spins, mu_s)
    E_Spirit = system.get_energy(p_state)

    return E_BF, E_Spirit

def test_gradient(p_state, mu = None):
    
    nos = system.get_nos(p_state)
    pos = np.array(geometry.get_positions(p_state)).reshape(nos, 3)
    spins = np.array(system.get_spin_directions(p_state)).reshape(nos, 3)

    simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_SIB, n_iterations=1)
    system.update_data(p_state)
    
    if type(mu) == type(None):
        mu_s = np.ones(len(pos))
    else:
        mu_s = mu

    Gradient_BF = Gradient_DDI_BF(pos, spins, mu_s)
    Gradient_Spirit = np.array(system.get_effective_field(p_state)).reshape(nos, 3)

    return Gradient_BF, Gradient_Spirit


def run():
    with state.State("input/input_brute_force.cfg", quiet = True) as p_state:
        #turn ddi on
        hamiltonian.set_ddi(p_state, 1)

        #turn everything else off
        hamiltonian.set_exchange(p_state, 0, [])
        hamiltonian.set_dmi(p_state, 0, [])
        hamiltonian.set_anisotropy(p_state, 0, [0,0,1])
        hamiltonian.set_boundary_conditions(p_state, [0,0,0])
        hamiltonian.set_field(p_state, 0, [0,0,1])

        #set a reasonable amount of basis cells
        geometry.set_n_cells(p_state, [5,5,5])

        configuration.plus_z(p_state)
        simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_SIB, n_iterations=1)
        E_Bf, E_Spirit = test_energy(p_state)
        Gradient_Bf, Gradient_Spirit = test_gradient(p_state)

        passed = True
        print('>>> Result 1: plus_z')
        print('E (Brute Force) = ', E_Bf)
        print('E (Spirit)      = ', E_Spirit)
        print('Avg. Grad (Brute Force) = ', np.mean(Gradient_Bf, axis = 0))
        print('Avg. Grad (Spirit)      = ', np.mean(Gradient_Spirit, axis = 0))
        if np.abs(E_Bf - E_Spirit) > tolerance:
            passed = False

        configuration.random(p_state)
        simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_SIB, n_iterations=1)
        E_Bf, E_Spirit = test_energy(p_state)
        Gradient_Bf, Gradient_Spirit = test_gradient(p_state)
        passed = True
        print('\n>>> Result 2: random')
        print('E (Brute Force) = ', E_Bf)
        print('E (Spirit)      = ', E_Spirit)
        print('Avg. Grad (Brute Force) = ', np.mean(Gradient_Bf, axis = 0))
        print('Avg. Grad (Spirit)      = ', np.mean(Gradient_Spirit, axis = 0))
        if np.abs(E_Bf - E_Spirit) > tolerance:
            passed = False

        configuration.hopfion(p_state, 4)
        simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_SIB, n_iterations=1)
        E_Bf, E_Spirit = test_energy(p_state)
        Gradient_Bf, Gradient_Spirit = test_gradient(p_state)
        passed = True
        print('\n>>> Result 3: hopfion')
        print('E (Brute Force) = ', E_Bf)
        print('E (Spirit)      = ', E_Spirit)
        print('Avg. Grad (Brute Force) = ', np.mean(Gradient_Bf, axis = 0))
        print('Avg. Grad (Spirit)      = ', np.mean(Gradient_Spirit, axis = 0))
        if np.abs(E_Bf - E_Spirit) > tolerance:
            passed = False
        return passed

if __name__ == "__main__":
    print(">>> Running Test: {}".format(name))
    print(">>> Information: {}".format(information))
    if run():
        print("\n    ---- RESULT ----")
        print("         Passed!")
    else:
        print("\n    ---- RESULT ----")        
        print("         Failed!")