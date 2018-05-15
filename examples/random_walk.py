
from random import randint, choice, shuffle


# Ugly hack to fix s.a imports
import sys
sys.path.append(sys.path[0] + "/..")
sys.path.append(sys.path[0] + "/../..")

from simulated_agency.simulation import Simulation
from simulated_agency.location import Location
from simulated_agency.agents import Agent as Walker
from simulated_agency.states import *
 

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
