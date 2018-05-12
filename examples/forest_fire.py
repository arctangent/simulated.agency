
from random import randint, choice, shuffle


# Ugly hack to fix s.a imports
import sys
sys.path.append(sys.path[0] + "/..")
sys.path.append(sys.path[0] + "/../..")

from simulated_agency.simulation import Simulation
from simulated_agency.location import Location
from simulated_agency.agents import Cell
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
            location = choice(tree.location.neighbourhood())
            # If that location is empty, put a tree there
            Cell(location, NotOnFire)


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
        for target in tree.location.neighbourhood():
            dice_roll = randint(1, 100)
            if dice_roll <= 50:
                # If that location has a tree, set it on fire
                if target.contents:
                    tree_to_burn = target.contents[0]
                    tree_to_burn.set_state(OnFire)





# Initialise simulation
simulation = Simulation(cell_size=40)
Location.simulation = simulation
Cell.simulation = simulation

# Constants
NUM_TREES = int(simulation.width * simulation.height * 0.5)

# Add some Trees to the simulation
for _ in range(0, NUM_TREES):
    Cell(simulation.random_location(), NotOnFire)
            


def loop():
    '''
    Event loop
    '''

    # Counter for image frame numbers
    simulation.counter += 1
    
    # Clear the canvas
    simulation.canvas.delete('all')

    # Go through the list of cells and tell each of them to do something
    shuffle(Cell.objects)
    for cell in Cell.objects:
        # Tell the cell to act
        cell.state.execute()
        simulation.draw(cell)

    # Save images
    if simulation.record_video:
        simulation.save_image('forest_fire')

    simulation.canvas.after(20, loop)
        
loop()
simulation.window.mainloop()