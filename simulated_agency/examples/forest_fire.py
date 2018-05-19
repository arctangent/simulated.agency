
from random import randint, choice

from ..simulation import Simulation
from ..location import Location
from ..agents import Cell as Tree
from ..states import State


# Define some custom states for this simulation

class NotOnFire(State):
    '''
    Represents a tree that is not on fire
    '''

    name = 'NOT_ON_FIRE'
    colour = 'green'
    glyph = '▲'

    def __init__(self, agent, **kwargs):
        ''' Initialise '''
        super().__init__(agent, **kwargs)
        # Trees start small
        self.agent.size = 0.4

    def handle(self):
        '''
        A tree not on fire may:
        (a) try to create a new adjancent tree
        (b) spontaneously set on fire (i.e. lightning strike)
        '''
        
        super().handle()

        tree = self.agent
        
        dice_roll = randint(1, 1000)

        if dice_roll == 1: 
            tree.replace_state(OnFire(tree, timer=3))

        elif dice_roll <= 100:
            # Grow a bit, up to a maximum size
            self.agent.size = min(self.agent.size + 0.1, 1.4)
            # Pick a direction to try to spread in
            location = choice(tree.location.neighbourhood())
            # If that location is empty, put a new tree there
            Tree(location, NotOnFire)
            


class OnFire(State):
    '''
    Represents a tree that is on fire
    '''

    name = 'ON_FIRE'
    colour = 'red'
    glyph = '▲'
    required_params = ['timer']

    def handle(self):
        '''
        A tree on fire will try to set fire to any adjancent trees.
        A tree on fire will burn down when its timer expires
        '''
        
        super().handle()

        tree = self.agent

        # If still on fire, see if the fire spreads
        for target in tree.location.neighbourhood():
            dice_roll = randint(1, 100)
            if dice_roll <= 25:
                # If that location has a tree, set it on fire if it isn't already on fire
                if target.contents:
                    tree_to_burn = target.contents[0]
                    if not tree_to_burn.is_in_state(OnFire):
                        tree_to_burn.replace_state(OnFire(tree_to_burn, timer=3))

    def handle_timeout(self):
        ''' When tree is finished burning we should remove it from the simulation '''
        tree = self.agent
        tree.destroy()




# Initialise simulation
simulation = Simulation(cell_size=40, name='ForestFire')

# Bind models to simulation
Location.simulation = simulation
Tree.simulation = simulation

# Add some Trees to the simulation
simulation.seed(Tree, 0.3, NotOnFire)

# Run the simulation
simulation.execute(Tree)

# Handle GUI events etc
simulation.window.mainloop()
