from spirit import state, simulation, constants, geometry

print("\n>>> TEST 1: Comparison to brute force calculation <<<\n")

inputfile = "test_cases/input/input_brute_force.cfg"
with state.State(inputfile, quiet = True) as p_state:
    simulation.start(p_state, simulation.METHOD_LLG, simulation.SOLVER_SIB, n_iterations=10, single_shot = True)
    simulation.single_shot(p_state)
    simulation.stop_all(p_state)


