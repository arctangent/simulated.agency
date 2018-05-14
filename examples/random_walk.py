
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
simulation = Simulation(cell_size=20)
Location.simulation = simulation
Walker.simulation = simulation

# Add some walkers to the simulation
simulation.seed(Walker, 0.3, MoveRandomly)


            


def loop():
    '''
    Event loop
    '''

    # Counter for image frame numbers
    simulation.counter += 1
    
    # Clear the canvas
    simulation.canvas.delete('all')

    # Go through the list of agents and tell each of them to do something
    shuffle(Walker.objects)
    for w in Walker.objects:
        # Tell the agent to act
        w.execute()
        simulation.draw(w)

    # Save images
    if simulation.record_video:
        simulation.save_image('random_walk')

    simulation.canvas.after(20, loop)
        
loop()
simulation.window.mainloop()