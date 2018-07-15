
from random import randint, choice

from simulated_agency.simulation import Simulation
from simulated_agency.agents import Locatable as Tree
from simulated_agency import glyphs
from simulated_agency.states import State


# Define some custom states for this simulation

class NotOnFire(State):
    '''
    Represents a tree that is not on fire
    '''

    name = 'NOT_ON_FIRE'
    colour = 'green'
    glyph = glyphs.BLACK_UP_POINTING_TRIANGLE

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

        # Grow tree a bit (up to max size)
        if tree.size <= 0.8:
            tree.size += 0.01
        
        # Did lightning strike?
        if randint(1, 100) == 1:
            # Oh no! The tree was struck by lightning.
            # It will burn for a variable amount of time.
            tree.replace_state(OnFire, timer=randint(6,10))
            return

        # Did the tree spawn another tree?
        if randint(1, 10) == 1:
            # Trees aren't fertile until they are 3
            if tree.age < 3:
                return
            # Pick a direction to try to spread in
            location = choice(tuple(tree.location.neighbourhood()))
            # If that location is empty, spawn a new tree there
            Tree(location, NotOnFire)

            


class OnFire(State):
    '''
    Represents a tree that is on fire
    '''

    name = 'ON_FIRE'
    colour = 'red'
    glyph = glyphs.BLACK_UP_POINTING_TRIANGLE
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

        # See if the fire spreads to neighbouring trees that are not on fire already
        for target in [t for t in tree.location.neighbours() if not t.is_in_state(OnFire)]:
            if randint(1, 4) == 1:
                # The tree_to_burn will burn for a variable amount of time
                target.replace_state(OnFire, timer=randint(6, 10))

    def handle_timeout(self):
        ''' When tree is finished burning we should remove it from the simulation '''
        tree = self.agent
        tree.destroy()


# Initialise simulation
simulation = Simulation(cell_size=40, name='ForestFire')

# Bind models to simulation
simulation.bind(Tree)

# Add some Trees to the simulation
simulation.seed(Tree, 0.15, NotOnFire)

# Run the simulation
simulation.execute(draw_locations=False)
