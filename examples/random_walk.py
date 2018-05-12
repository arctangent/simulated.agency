
from random import randint, choice, shuffle


# Ugly hack to fix s.a imports
import sys
sys.path.append(sys.path[0] + "/..")
sys.path.append(sys.path[0] + "/../..")

from simulated_agency.world import World
from simulated_agency.location import Location
from simulated_agency.agent import Agent
from simulated_agency import states
 

# Initialise world
world = World(cell_size=20)
Location.world = world

# Constants
NUM_WALKERS = int(world.width * world.height * 0.3)

# A Walker is identical to the Agent class (for now)
Walker = Agent

# Specify the World the Walkers live in
Walker.world = world

# Add some walkers to the world
for _ in range(0, NUM_WALKERS):
    x = randint(0, world.width - 1)
    y = randint(0, world.height -1)
    Walker(Location(x, y), states.MovingRandomly)
            


while True:
    '''
    Event loop
    '''

    # Counter for image frame numbers
    world.counter += 1
    
    # Clear the canvas
    world.canvas.delete('all')

    # Go through the list of agents and tell each of them to do something
    shuffle(Walker.objects)
    for agent in Walker.objects:
        # Tell the agent to act
        agent.state.execute()
        world.draw(agent)

    # Update the canvas
    world.canvas.after(20)
    world.canvas.update()

    # Save images
    if world.record_video:
        world.save_image('random_walk')
        

world.window.mainloop()