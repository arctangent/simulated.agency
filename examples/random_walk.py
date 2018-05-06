
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

# Constants
NUM_WALKERS = int(world.width * world.height * 0.3)

# Add some locations to the world - specifically, a simple grid
Location.world = world
for x in range(0, world.width):
    for y in range(0, world.height):
        world.locations[x, y] = Location(x, y)

# A Walker is identical to the Agent class (for now)
Walker = Agent

# Specify the World the Walkers live in
Walker.world = world

# Add some walkers to the world
for _ in range(0, NUM_WALKERS):
    x = randint(0, world.width - 1)
    y = randint(0, world.height -1)
    location = world.locations[x, y]
    if not location.is_full():
        walker = Walker(location)
        location.contents.append(walker)
        walker.set_state(states.MovingRandomly)
        world.agents.append(walker)
            


while True:
    '''
    Event loop
    '''

    # Counter for image frame numbers
    world.counter += 1
    
    # Clear the canvas
    world.canvas.delete('all')

    # Go through the list of agents and tell each of them to do something
    shuffle(world.agents)
    for agent in world.agents:
        # Tell the agent to act
        agent.state.execute()
        world.draw(agent.location.x, agent.location.y, fill=agent.state.colour)

    # Update the canvas
    world.canvas.after(20)
    world.canvas.update()

    # Save images
    if world.record_video:
        world.save_image('random_walk')
        

world.window.mainloop()