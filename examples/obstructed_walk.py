
from simulated_agency.simulation import Simulation
from simulated_agency.agents import Mobile as Walker
from simulated_agency.states import *
 

# Initialise simulation
simulation = Simulation(name='RandomWalk')

# Bind models to simulation
simulation.bind(Walker)

# Add obstacle
simulation.create_obstruction_rectangle(5, 10, 20, 5)

# Add some walkers to the simulation
simulation.seed(Walker, 0.3, MoveRandomly)

# Run the simulation
simulation.execute()
