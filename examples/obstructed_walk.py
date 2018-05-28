
from simulated_agency.simulation import Simulation
from simulated_agency.agents import Mobile as Walker
from simulated_agency.states import *
 

# Initialise simulation
simulation = Simulation(cell_size=20, name='RandomWalk')

# Bind models to simulation
Walker.simulation = simulation

# Add obstacle
simulation.create_obstruction_rectangle(5, 10, 20, 5)

# Add some walkers to the simulation
simulation.seed(Walker, 0.3, MoveRandomly)

# Run the simulation
simulation.execute(Walker)

# Handle GUI events etc
simulation.window.mainloop()
