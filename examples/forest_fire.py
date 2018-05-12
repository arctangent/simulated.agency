
from random import randint, choice, shuffle


# Ugly hack to fix s.a imports
import sys
sys.path.append(sys.path[0] + "/..")
sys.path.append(sys.path[0] + "/../..")

from simulated_agency.simulation import Simulation
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
        simulation = tree.simulation

        dice_roll = randint(1, 1000)

        if dice_roll == 1:
            tree.set_state(OnFire)

        elif dice_roll <= 100:
            # Pick a direction to try to spread in
            location = choice(tree.location.neighbours())
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
        simulation = tree.simulation

        # Check if burned down yet
        self.timer -= 1
        if self.timer == 0:
            # Remove self from the simulation (i.e. burn down)
            tree.destroy()
            return

        # If still on fire, see if the fire spreads
        for target in tree.location.neighbours():
            dice_roll = randint(1, 100)
            if dice_roll <= 50:
                # If that location has a tree, set it on fire
                if target.contents:
                    tree_to_burn = target.contents[0]
                    tree_to_burn.set_state(OnFire)





# Initialise simulation
simulation = Simulation(cell_size=40)
Location.simulation = simulation

# Constants
NUM_TREES = int(simulation.width * simulation.height * 0.5)

# A Tree is identical to the Agent class (for now)
Tree = Agent

# Specify the Simulation the Trees live in
Tree.simulation = simulation

# Add some Trees to the simulation
for _ in range(0, NUM_TREES):
    Tree(simulation.random_location(), NotOnFire)
            


while True:
    '''
    Event loop
    '''

    # Counter for image frame numbers
    simulation.counter += 1
    
    # Clear the canvas
    simulation.canvas.delete('all')

    # Go through the list of agents and tell each of them to do something
    shuffle(Tree.objects)
    for agent in Tree.objects:
        # Tell the agent to act
        agent.state.execute()
        simulation.draw(agent)

    # Update the canvas
    simulation.canvas.after(20)
    simulation.canvas.update()

    # Save images
    if simulation.record_video:
        simulation.save_image('forest_fire')
        

simulation.window.mainloop()