from spirit import state, simulation, constants, geometry, system, hamiltonian, configuration
import numpy as np
from .test import Test

class Test_Brute_Force(Test):

    name = "Comparison to brute force (energy)"
    inputfile = "test_cases/input/input_brute_force.cfg"

    def test_energy(self, p_state):
        nos = system.get_nos(p_state)
        pos = np.array(geometry.get_positions(p_state)).reshape(nos, 3)
        spins = np.array(system.get_spin_directions(p_state)).reshape(nos, 3)

        E_BF = self.E_DDI_BF(pos, spins)
        E_Spirit = system.get_energy(p_state)

        return E_BF, E_Spirit

    def run(self):
        passed = True

        with state.State(self.inputfile, quiet = True) as p_state:
            hamiltonian.set_boundary_conditions(p_state, [0, 0, 0], idx_image=-1, idx_chain=-1)
            hamiltonian.set_field(p_state, 0.0, [0, 0 , 1])
            hamiltonian.set_anisotropy(p_state, 0.0, [0, 0 , 1])
            hamiltonian.set_anisotropy(p_state, 0.0, [0, 0 , 1])

            # simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_SIB, n_iterations=10, single_shot = True)

            configuration.plus_z(p_state)
            system.update_data(p_state)
            E_Bf, E_Spirit = self.test_energy(p_state)
            passed = True
            print('>>> Result 1: plus_z')
            print('Brute Force = ', E_Bf)
            print('Spirit      = ', E_Spirit)
            if np.abs(E_Bf - E_Spirit) > 1e-6:
                passed = False

            configuration.random(p_state)
            system.update_data(p_state)
            E_Bf, E_Spirit = self.test_energy(p_state)
            passed = True
            print('\n>>> Result 2: random')
            print('Brute Force = ', E_Bf)
            print('Spirit      = ', E_Spirit)
            if np.abs(E_Bf - E_Spirit) > 1e-6:
                passed = False

            configuration.hopfion(p_state, 4)
            system.update_data(p_state)
            E_Bf, E_Spirit = self.test_energy(p_state)
            passed = True
            print('\n>>> Result 3: hopfion')
            print('Brute Force = ', E_Bf)
            print('Spirit      = ', E_Spirit)
            if np.abs(E_Bf - E_Spirit) > 1e-6:
                passed = False
            
            return passed




