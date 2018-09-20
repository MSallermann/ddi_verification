from spirit import state, simulation, constants, parameters , geometry, system, hamiltonian, configuration
import numpy as np
from .test import Test

class Test_Saturated_Film(Test):

    name = "Uniformly magnetized film"
    inputfile = "test_cases/input/input_saturated_film.cfg"
    information = "Test the field of a 2D-film that is uniformly magnetized in z-direction. The result is compared to the theoretical direct sum!"

    def run(self, enable_output = True):
        passed = True
        self.inputfile = "test_cases/input/input_saturated_film.cfg"

        theory = 0.5
        N_ITERATIONS = 1
        system_sizes = [10 * (i+1) for i in range(5)]
        field_center = []
        E = []

        for size in system_sizes:
            with state.State(self.inputfile) as p_state:
                parameters.llg.set_output_general(p_state, any=False)
                geometry.set_n_cells(p_state, [size, size, 1])
                configuration.plus_z(p_state)
                nos = system.get_nos(p_state)

                simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_VP, n_iterations = 1)

                Gradient_Spirit = np.array(system.get_effective_field(p_state)).reshape(nos, 3)
                E_Spirit = system.get_energy(p_state)

                field_center.append(Gradient_Spirit[int(size/2 + size/2 * size)])
                E.append(E_Spirit)
                
        if enable_output:
            with open('output_'+self.name+'.txt', 'w') as out:
                out.write("#system_size, field_center_z, energy\n")
                for i in range(len(E)):
                    out.write("{0}, {1}, {2}\n".format(system_sizes[i], field_center[i][2], E[i]))








