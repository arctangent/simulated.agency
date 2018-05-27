
from random import randint, choice

from simulated_agency.simulation import Simulation
from simulated_agency.agents import Cell as Tree
from simulated_agency.states import State


# Define some custom states for this simulation

class NotOnFire(State):
    '''
    Represents a tree that is not on fire
    '''

    name = 'NOT_ON_FIRE'
    colour = 'green'
    glyph = '▲'
    size = 0.4

    def __init__(self, agent, **kwargs):
        ''' Initialise '''
        super().__init__(agent, **kwargs)
        # Trees start small
        self.size = 0.4

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
            # Oh no! The tree was struck by lightning.
            # It will burn for a variable amount of time.
            tree.replace_state(OnFire(tree, timer=randint(6,10)))

        elif dice_roll <= 100:
            # Grow tree a bit
            self.agent.size += 0.25
            # Trees aren't fertile until they are 3
            if self.agent.age < 3:
                return
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
    size = 0.4
    required_params = ['timer']

    def handle(self):
        '''
        A tree on fire for 5 turns or more will try to set
        fire to any adjancent trees.
        A tree on fire will burn down when its timer expires
        '''
        
        super().handle()

        tree = self.agent

        # It always takes 2 turns of yellow burning
        # before we get to orange burning
        if self.age <= 2:
            self.colour = "yellow"
            return

        # It always takes 2 turns of orange buring
        # before we get to red burning
        if self.age <= 4:
            self.colour = "orange"
            return

        # Red burning trees are able to spread fire
        self.colour = "red"

        # See if the fire spreads
        for target in tree.location.neighbourhood():
            dice_roll = randint(1, 100)
            if dice_roll <= 25:
                # If that location has a tree, set it on fire if it isn't already on fire
                if target.contents:
                    tree_to_burn = target.contents[0]
                    if not tree_to_burn.is_in_state(OnFire):
                        # The tree_to_burn will burn for a variable amount of time
                        tree_to_burn.replace_state(OnFire(tree_to_burn, timer=randint(6, 10)))

    def handle_timeout(self):
        ''' When tree is finished burning we should remove it from the simulation '''
        tree = self.agent
        tree.destroy()




# Initialise simulation
simulation = Simulation(cell_size=40, name='ForestFire')

# Bind models to simulation
Tree.simulation = simulation

# Add some Trees to the simulation
simulation.seed(Tree, 0.3, NotOnFire)

# Run the simulation
simulation.execute(Tree)

# Handle GUI events etc
simulation.window.mainloop()
