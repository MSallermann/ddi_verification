from spirit import state, simulation, constants, geometry, system, hamiltonian, configuration
import numpy as np
from .test import Test

class Test_Brute_Force(Test):

    name = "Comparison to brute force (energy)"
    information = "Comparison to Brute Force Calculations of the energy. Note: The Gradient is also shown, but may be different from the Brute Force Gradient because spirit only takes the component orthogonal to the spin."
    inputfile = "test_cases/input/input_brute_force.cfg"

    def run(self):
        passed = True

        with state.State(self.inputfile, quiet = True) as p_state:

            configuration.plus_z(p_state)
            # simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_SIB, n_iterations=1)
            system.update_data(p_state)

            E_Bf, E_Spirit = self.test_energy(p_state)

            Gradient_Bf, Gradient_Spirit = self.test_gradient(p_state)

            passed = True
            print('>>> Result 1: plus_z')
            print('E (Brute Force) = ', E_Bf)
            print('E (Spirit)      = ', E_Spirit)
            print('Avg. Grad (Brute Force) = ', np.mean(Gradient_Bf, axis = 0))
            print('Avg. Grad (Spirit)      = ', np.mean(Gradient_Spirit, axis = 0))
            if np.abs(E_Bf - E_Spirit) > 1e-4:
                passed = False

            configuration.random(p_state)
            simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_SIB, n_iterations=1)
            system.update_data(p_state)
            E_Bf, E_Spirit = self.test_energy(p_state)
            Gradient_Bf, Gradient_Spirit = self.test_gradient(p_state)
            passed = True
            print('\n>>> Result 2: random')
            print('E (Brute Force) = ', E_Bf)
            print('E (Spirit)      = ', E_Spirit)
            print('Avg. Grad (Brute Force) = ', np.mean(Gradient_Bf, axis = 0))
            print('Avg. Grad (Spirit)      = ', np.mean(Gradient_Spirit, axis = 0))
            if np.abs(E_Bf - E_Spirit) > 1e-4:
                passed = False

            configuration.hopfion(p_state, 4)
            simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_SIB, n_iterations=1)
            system.update_data(p_state)
            E_Bf, E_Spirit = self.test_energy(p_state)
            Gradient_Bf, Gradient_Spirit = self.test_gradient(p_state)
            passed = True
            print('\n>>> Result 3: hopfion')
            print('E (Brute Force) = ', E_Bf)
            print('E (Spirit)      = ', E_Spirit)
            print('Avg. Grad (Brute Force) = ', np.mean(Gradient_Bf, axis = 0))
            print('Avg. Grad (Spirit)      = ', np.mean(Gradient_Spirit, axis = 0))
            if np.abs(E_Bf - E_Spirit) > 1e-4:
                passed = False
            
            return passed




