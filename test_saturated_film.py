if __name__ == "__main__":
    path_to_spirit_pkg = "/Users/sallermann/Coding/spirit/core/python"
    import sys
    sys.path.append(path_to_spirit_pkg)

from spirit import state
from spirit import simulation
from spirit import constants
from spirit import geometry
from spirit import parameters
from spirit import system
from spirit import hamiltonian
from spirit import configuration
import numpy as np

name = "Uniformly magnetized film"
information = "Test the field of a 2D-film that is uniformly magnetized in z-direction. The result is compared to the theoretical direct sum!"
outputfile = "output_saturated_film.txt"
enable_output = False
system_sizes = [10 * (i+1) for i in range(5)]
theory = 0.5


def run(enable_output = True):
    passed = True
    field_center = []
    E = []

    for size in system_sizes:
        with state.State("") as p_state:
            parameters.llg.set_output_general(p_state, any=False)
            
            #turn ddi on
            hamiltonian.set_ddi(p_state, 1)

            #turn everything else off
            hamiltonian.set_exchange(p_state, 0, [])
            hamiltonian.set_dmi(p_state, 0, [])
            hamiltonian.set_anisotropy(p_state, 0, [0,0,1])
            hamiltonian.set_boundary_conditions(p_state, [0,0,0])
            hamiltonian.set_field(p_state, 0, [0,0,1])

            geometry.set_n_cells(p_state, [size, size, 1])
            
            configuration.plus_z(p_state)
            nos = system.get_nos(p_state)
            simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_VP, n_iterations = 1)
            Gradient_Spirit = np.array(system.get_effective_field(p_state)).reshape(nos, 3)
            E_Spirit = system.get_energy(p_state)
            field_center.append(Gradient_Spirit[int(size/2 + size/2 * size)])
            E.append(E_Spirit)
            
        if enable_output:
            with open(outputfile, 'w') as out:
                out.write("#system_size, field_center_z, energy\n")
                for i in range(len(E)):
                    out.write("{0}, {1}, {2}\n".format(system_sizes[i], field_center[i][2], E[i]))

if __name__ == "__main__":
    print(">>> Running Test: {}".format(name))
    print(">>> Information: {}".format(information))
    if run():
        print("\n    ---- RESULT ----")
        print("           Passed!")
    else:
        print("\n    ---- RESULT ----")        
        print("         Failed!")




