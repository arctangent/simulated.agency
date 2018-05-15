
from ..simulation import Simulation
from ..location import Location
from ..agents import Agent as Walker
from ..states import *
 

# Initialise simulation
simulation = Simulation(cell_size=20, name='RandomWalk')

# Bind models to simulation
Location.simulation = simulation
Walker.simulation = simulation

# Add some walkers to the simulation
simulation.seed(Walker, 0.3, MoveRandomly)

# Run the simulation
simulation.execute(Walker)

# Handle GUI events etc
simulation.window.mainloop()
