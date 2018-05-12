
from random import randint, choice, shuffle


# Ugly hack to fix s.a imports
import sys
sys.path.append(sys.path[0] + "/..")
sys.path.append(sys.path[0] + "/../..")

from simulated_agency.simulation import Simulation
from simulated_agency.location import Location
from simulated_agency.agents import Agent
from simulated_agency import states
 

# Initialise simulation
simulation = Simulation(cell_size=20)
Location.simulation = simulation

# Constants
NUM_WALKERS = int(simulation.width * simulation.height * 0.3)

# A Walker is identical to the Agent class (for now)
Walker = Agent

# Specify the Simulation the Walkers live in
Walker.simulation = simulation

# Add some walkers to the simulation
for _ in range(0, NUM_WALKERS):
    Walker(simulation.random_location(), states.MovingRandomly)
            


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
    for agent in Walker.objects:
        # Tell the agent to act
        agent.state.execute()
        simulation.draw(agent)

    # Save images
    if simulation.record_video:
        simulation.save_image('random_walk')

    simulation.canvas.after(20, loop)
        
loop()
simulation.window.mainloop()