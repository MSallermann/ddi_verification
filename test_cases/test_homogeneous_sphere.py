from spirit import state, simulation, constants, geometry, system, hamiltonian, configuration
from .test import Test
import numpy as np

class Test_Homogeneous_Sphere(Test):
    name = "Uniformly magnetized sphere_20"
    inputfile = "test_cases/input/input_homogeneous_sphere_20.cfg"

    def get_field_in_sphere(self, field, pos, radius, center):
        in_sphere = np.linalg.norm(pos - center, axis=1) < radius
        return field[in_sphere]

    def run(self):
        passed = True

        with state.State(self.inputfile, quiet = True) as p_state:
            configuration.plus_z(p_state)
            system.update_data(p_state)

            simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_SIB, n_iterations=1)

            nos = system.get_nos(p_state)
            field = np.array(system.get_effective_field(p_state)).reshape(nos, 3)
            pos = np.array(geometry.get_positions(p_state)).reshape(nos, 3)

            l_cube = 50
            center = np.array([l_cube/2, l_cube/2, l_cube/2], dtype = int)

            field_in_sphere = self.get_field_in_sphere(field, pos, l_cube/2, center)

            mean_grad = np.mean(field_in_sphere, axis=0)
            deviation = np.std(field_in_sphere - mean_grad, axis=0)

            theory = np.array([0, 0, 1]) * 2/3 * self.mu_B**2 * self.mu_0 * 1e30

            # print(len(field))
            # print(len(field_in_sphere))
            # print(len(field) - len(field_in_sphere))

            print(np.mean(field, axis=0))

            # print(mean_grad)
            # print(deviation)
            # print(theory)

        return passed










    
