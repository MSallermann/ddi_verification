from spirit import state, simulation, constants, geometry, system, hamiltonian, configuration
import numpy as np

mu_0 = 2.01335452495e-28
mu_B = 0.0578838177025
name = "Energy comparison to brute force calculation"

def E_DDI_BF(pos, spins, mu_s = 1):
    E = 0
    mult = - mu_0 * mu_B**2 / (4 * np.pi * 1e-30) 
    for i in range(len(pos)):
        for j in range(i+1, len(pos)):
            r = pos[i] - pos[j]
            d = np.linalg.norm(r)
            r /= d
            # E += mult/d**3 * mu[i] * mu[j] * ( 3 * np.dot(spins[i], r) * np.dot(spins[j], r) - np.dot(spins[i], spins[j]) )
            E += mult/d**3 * mu_s**2 * ( 3 * np.dot(spins[i], r) * np.dot(spins[j], r) - np.dot(spins[i], spins[j]) )
    return E

def test_energy(p_state):
    nos = system.get_nos(p_state)
    pos = np.array(geometry.get_positions(p_state)).reshape(nos, 3)
    spins = np.array(system.get_spin_directions(p_state)).reshape(nos, 3)

    E_BF = E_DDI_BF(pos, spins)
    E_Spirit = system.get_energy(p_state)

    return E_BF, E_Spirit

def run():
    inputfile = "test_cases/input/input_brute_force.cfg"
    passed = True

    with state.State(inputfile, quiet = True) as p_state:
        hamiltonian.set_boundary_conditions(p_state, [0, 0, 0], idx_image=-1, idx_chain=-1)

        hamiltonian.set_field(p_state, 0.0, [0, 0 , 1])
        hamiltonian.set_anisotropy(p_state, 0.0, [0, 0 , 1])
        hamiltonian.set_anisotropy(p_state, 0.0, [0, 0 , 1])

        # simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_SIB, n_iterations=10, single_shot = True)

        configuration.plus_z(p_state)
        system.update_data(p_state)
        E_Bf, E_Spirit = test_energy(p_state)
        passed = True
        print('\n>>> Result 1: plus_z')
        print('Brute Force = ', E_Bf)
        print('Spirit      = ', E_Spirit)
        if np.abs(E_Bf - E_Spirit) > 1e-6:
            passed = False

        configuration.random(p_state)
        system.update_data(p_state)
        E_Bf, E_Spirit = test_energy(p_state)
        passed = True
        print('\n>>> Result 2: random')
        print('Brute Force = ', E_Bf)
        print('Spirit      = ', E_Spirit)
        if np.abs(E_Bf - E_Spirit) > 1e-6:
            passed = False

        configuration.hopfion(p_state, 4)
        system.update_data(p_state)
        E_Bf, E_Spirit = test_energy(p_state)
        passed = True
        print('\n>>> Result 3: hopfion')
        print('Brute Force = ', E_Bf)
        print('Spirit      = ', E_Spirit)
        if np.abs(E_Bf - E_Spirit) > 1e-6:
            passed = False
        
        return passed




