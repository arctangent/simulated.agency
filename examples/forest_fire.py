
from random import randint, choice, shuffle


# Ugly hack to fix s.a imports
import sys
sys.path.append(sys.path[0] + "/..")
sys.path.append(sys.path[0] + "/../..")

from simulated_agency.world import World
from simulated_agency.location import Location
from simulated_agency.agent import Agent
from simulated_agency.states import State


# Define some custom states for this simulation

class NotOnFire(State):
    '''
    Represents a tree that is not on fire
    '''

    def __init__(self, agent):
        super().__init__(agent)
        self.name = 'NOT_ON_FIRE'
        self.colour = 'green'

    def execute(self):
        '''
        A tree not on fire may:
        (a) try to create a new adjancent tree
        (b) spontaneously set on fire (i.e. lightning strike)
        '''

        tree = self.agent
        world = tree.world

        dice_roll = randint(1, 1000)

        if dice_roll == 1:
            tree.set_state(OnFire)

        elif dice_roll <= 100:
            # Pick a direction to try to spread in
            dice_roll = randint(1, 4)
            if dice_roll == 1:
                location = tree.location.up()
            elif dice_roll == 2:
                location = tree.location.down()
            elif dice_roll == 3:
                location = tree.location.left()
            elif dice_roll == 4:
                location = tree.location.right()

            # If that location is empty, put a tree there
            Tree(location, NotOnFire)


class OnFire(State):
    '''
    Represents a tree that is on fire
    '''

    def __init__(self, agent):
        super().__init__(agent)
        self.name = 'ON_FIRE'
        self.colour = 'red'
        self.timer = randint(1, 3)

    def execute(self):
        '''
        A tree on fire will try to set fire to any adjancent trees.
        A tree on fire will burn down when its timer expires
        '''

        tree = self.agent
        world = tree.world

        # Check if burned down yet
        self.timer -= 1
        if self.timer == 0:
            # Remove self from the world (i.e. burn down)
            tree.destroy()
            return

        # If still on fire, see if the fire spreads

        adjacent_cells = [
            tree.location.up(),
            tree.location.down(),
            tree.location.left(),
            tree.location.right()
        ]

        for target in adjacent_cells:
            dice_roll = randint(1, 100)
            if dice_roll <= 50:
                # If that location has a tree, set it on fire
                if target.contents:
                    tree_to_burn = target.contents[0]
                    tree_to_burn.set_state(OnFire)





# Initialise world
world = World(cell_size=40)

# Constants
NUM_TREES = int(world.width * world.height * 0.5)

# Add some locations to the world - specifically, a simple grid
Location.world = world
for x in range(0, world.width):
    for y in range(0, world.height):
        world.locations[x, y] = Location(x, y)

# A Tree is identical to the Agent class (for now)
Tree = Agent

# Specify the World the Trees live in
Tree.world = world

# Add some Trees to the world
for _ in range(0, NUM_TREES):
    x = randint(0, world.width - 1)
    y = randint(0, world.height -1)
    location = world.locations[x, y]
    Tree(location, NotOnFire)
            


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
        world.draw(agent)

    # Update the canvas
    world.canvas.after(20)
    world.canvas.update()

    # Save images
    if world.record_video:
        world.save_image('forest_fire')
        

world.window.mainloop()