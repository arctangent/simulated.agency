
from simulated_agency.simulation import Simulation
from simulated_agency.agents import Mobile as Walker
from simulated_agency.states import *
 

# Initialise simulation
simulation = Simulation(cell_size=20, name='RandomWalk')

# Bind models to simulation
Walker.simulation = simulation

# Add some walkers to the simulation
simulation.seed(Walker, 0.3, MoveRandomly)

# Run the simulation
simulation.execute(Walker, draw_locations=False)

# Handle GUI events etc
simulation.window.mainloop()
