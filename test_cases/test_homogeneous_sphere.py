from spirit import state, simulation, constants, geometry, system, hamiltonian, configuration
from .test import Test
import numpy as np

class Test_Homogeneous_Sphere(Test):
    name = "Uniformly magnetized sphere_100"
    inputfile = "test_cases/input/input_homogeneous_sphere_100.cfg"
    information = 'The field inside a uniformly magnetized sphere is compared with a theoretical result. '
                
    def run(self):
        passed = True
        l_cube = 100
        radius = l_cube/4

        with state.State(self.inputfile, quiet = True) as p_state:
            configuration.plus_z(p_state)
            simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_SIB, n_iterations=1)
            system.update_data(p_state)

            #query some quantities
            nos   = system.get_nos(p_state)
            field = np.array(system.get_effective_field(p_state)).reshape(nos, 3)
            pos   = np.array(geometry.get_positions(p_state)).reshape(nos, 3)
            spins = np.array(system.get_spin_directions(p_state)).reshape(nos, 3)

            #get quantitities in sphere
            center = np.array([l_cube/2, l_cube/2, l_cube/2], dtype = int)
            idx_in_sphere = np.linalg.norm(pos - center, axis=1) <= radius
            mu_s = np.array( [ 1 if idx_in_sphere[i] else 0 for i in range(nos)] )

            # field_bf = self.Gradient_DDI_BF(pos, spins, mu_s)
            # field_bf_in_sphere = field_bf[idx_in_sphere]

            field_in_sphere = field[idx_in_sphere]

            # deviation_sphere = np.std(field_in_sphere - mean_grad_sphere, axis=0)

            theory = np.array([0, 0, 1]) * 2/3 * self.mu_0 * self.mu_B * self.mu_B * 1e30

            print("Mean field                  = ", np.mean(field/self.mu_B, axis=0))
            # print("Mean field (BF)             = ", np.mean(field_bf/self.mu_B, axis=0))
            print("Mean field in sphere        = ", np.mean(field_in_sphere/self.mu_B, axis=0))
            # print("Mean field in sphere (BF)   = ", np.mean(field_bf_in_sphere/self.mu_B, axis=0))
            print("Theory                      = ", theory)


        return passed






    
