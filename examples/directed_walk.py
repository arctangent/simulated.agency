
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
simulation = Simulation(cell_size=8)
Location.simulation = simulation

# Constants
NUM_WALKERS = int(simulation.width * simulation.height * 0.1)

# A Walker is identical to the Agent class (for now)
Walker = Agent

# Specify the Simulation the Walkers live in
Walker.simulation = simulation

# A static target is the same thing as a "Dead" walker
Static = states.Dead
Static.colour = 'cyan'
x = int(simulation.width / 4)
y = int(simulation.height / 4)
target = Walker(Location(x, y), Static)

# Add some walkers to the simulation
for _ in range(0, NUM_WALKERS):
    Walker(simulation.random_location(), states.MovingTowards, target=target)
            


def loop():
    '''
    Event loop
    '''

    # Counter for image frame numbers
    simulation.counter += 1
    
    # Clear the canvas
    simulation.canvas.delete('all')

    # Change the target from time to time
    change_target = False
    dice_roll = randint(1, 30)
    if dice_roll == 1:
        change_target = True
        target.location = simulation.random_location()
    
    # Go through the list of agents and tell each of them to do something
    shuffle(Walker.objects)
    for agent in Walker.objects:
        if change_target:
            # Don't change the state of our target
            if agent is target:
                continue
            agent.set_state(states.MovingTowards, target=target)
        # Tell the agent to act
        agent.state.execute()
        simulation.draw(agent)

    # Draw the target last
    simulation.draw(target)

    # Save images
    if simulation.record_video:
        simulation.save_image('directed_walk')

    simulation.canvas.after(20, loop)
        
loop()
simulation.window.mainloop()