
from random import randint, choice, shuffle


# Ugly hack to fix s.a imports
import sys
sys.path.append(sys.path[0] + "/..")
sys.path.append(sys.path[0] + "/../..")

from simulated_agency.simulation import Simulation
from simulated_agency.location import Location
from simulated_agency.agents import Cell as Tree
from simulated_agency.states import StateMachine, State


# Define some custom states for this simulation

class NotOnFire(State):
    '''
    Represents a tree that is not on fire
    '''

    name = 'NOT_ON_FIRE'
    colour = 'green'

    def execute(self, tree):
        '''
        A tree not on fire may:
        (a) try to create a new adjancent tree
        (b) spontaneously set on fire (i.e. lightning strike)
        '''
        #super().execute(tree)
        dice_roll = randint(1, 1000)

        if dice_roll == 1:
            tree.set_state(OnFire, timer=3)

        elif dice_roll <= 100:
            # Pick a direction to try to spread in
            location = choice(tree.location.neighbourhood())
            # If that location is empty, put a tree there
            Tree(location, NotOnFire)


class OnFire(State):
    '''
    Represents a tree that is on fire
    '''

    name = 'ON_FIRE'
    colour = 'red'
    required_params = ['timer']

    def execute(self, tree):
        '''
        A tree on fire will try to set fire to any adjancent trees.
        A tree on fire will burn down when its timer expires
        '''
        #super().execute(tree)
        # Check if burned down yet
        tree.memory['timer'] -= 1
        if tree.memory['timer'] == 0:
            # Remove self from the simulation (i.e. burn down)
            tree.destroy()
            return

        # If still on fire, see if the fire spreads
        for target in tree.location.neighbourhood():
            dice_roll = randint(1, 100)
            if dice_roll <= 25:
                # If that location has a tree, set it on fire if it isn't already on fire
                if target.contents:
                    tree_to_burn = target.contents[0]
                    if not tree_to_burn.state == OnFire:
                        tree_to_burn.set_state(OnFire, timer=3)


# Initialise state machine
state_machine = StateMachine()
state_machine.register(OnFire)
state_machine.register(NotOnFire)


# Initialise simulation
simulation = Simulation(cell_size=20)
Location.simulation = simulation
Tree.simulation = simulation
Tree.state_machine = state_machine

# Constants
NUM_TREES = int(simulation.width * simulation.height * 0.5)

# Add some Trees to the simulation
for _ in range(0, NUM_TREES):
    Tree(simulation.random_location(), NotOnFire)
            


def loop():
    '''
    Event loop
    '''

    # Counter for image frame numbers
    simulation.counter += 1
    
    # Clear the canvas
    simulation.canvas.delete('all')

    # Go through the list of trees and tell each of them to do something
    shuffle(Tree.objects)
    for tree in Tree.objects:
        # Tell the tree to act
        tree.execute()
        simulation.draw(tree)

    # Save images
    if simulation.record_video:
        simulation.save_image('forest_fire')

    simulation.canvas.after(20, loop)
        
loop()
simulation.window.mainloop()