from spirit import state, simulation, constants, geometry, system, hamiltonian, configuration
import numpy as np
from .test import Test

class Test_Saturated_Film_Cutout(Test):

    name = "Uniformly magnetized film with cutout"
    inputfile = "test_cases/input/input_saturated_film_cutout.cfg"
    information = "Test the field of a 2D-film that is uniformly magnetized in z-direction. The field is tested at the center of a circular cutout and compared with a theoretical result, where the magnetization is approximated as continuous"

    def run(self):
        passed = True
        l=1000

        with state.State(self.inputfile, quiet = True) as p_state:

            configuration.plus_z(p_state)
            system.update_data(p_state)
            nos = system.get_nos(p_state)

            E_Spirit = system.get_energy(p_state)

            simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_SIB, n_iterations=1)
            Gradient_Spirit = np.array(system.get_effective_field(p_state)).reshape(nos, 3)
            field_center = Gradient_Spirit[int(l/2 + l/2 * l)]

            #Theory
            # avg_field_theory = 2 * np.pi / (1e-10) * self.mu_s* (self.mu_0 * self.mu_B**2) / (4*np.pi * 1e-30)
            field_center_theory = - self.mu_0 * self.mu_B / (2 * 20 * 1e-10) * (self.mu_B * 1e20) * np.array([0, 0, 1])

            print('Result:')
            print('Field (center)              = ', field_center)
            print('Field (center) (Theory)     = ', field_center_theory)
           
            if np.linalg.norm(np.linalg.norm(field_center - field_center_theory) > 1e-2):
                passed = False

            return passed




