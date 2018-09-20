from spirit import state, simulation, constants, geometry, system, hamiltonian, configuration
from .test import Test
import numpy as np

class Test_mu_s_Scaling(Test):
    name = "mu_s scaling"
    info = "Test if the energy scales correctly with mu_s^2."
    inputfile1 = "test_cases/input/input_mu_s_scaling_1.cfg"
    inputfile2 = "test_cases/input/input_mu_s_scaling_2.cfg"

    def run(self):
        passed = True

        with state.State(self.inputfile1, quiet = True) as p_state:
            configuration.plus_z(p_state)
            system.update_data(p_state)
            E_1 = system.get_energy(p_state)
            print('>>> Result 1: mu_s = 1')
            print('E_DDI = ', E_1)
        
        with state.State(self.inputfile2, quiet = True) as p_state:
            configuration.plus_z(p_state)
            system.update_data(p_state)
            E_2 = system.get_energy(p_state)
            print('\n>>> Result 2: mu_s = 2')
            print('E_DDI = ', E_2)
        
        if np.abs(E_1 * 2**2 - E_2) > 1e-1:
            passed = False

        return passed