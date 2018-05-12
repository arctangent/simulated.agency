
from random import randint

from .location import Location
from .mixins import Mobile

from .states import Dead, Waiting, MovingRandomly, MovingTowards


class Agent(Mobile):
    '''
    Represents an agent that can move around in the Simulation.
    '''
        
    def __init__(self, location, state=None, **state_params):
        '''
        Initialise
        '''
        super().__init__(location)

        # State - assumed to be random motion if not specified
        state = state or MovingRandomly
        self.set_state(state, **state_params)
        
        
    def set_state(self, state_class, **state_params):
        '''
        This function ensures that necessary initialisation
        actions are carried out when an Agent changes state.
        '''
        
        # We pass the kwargs to the state class so it can init correctly
        self.state = state_class(self, **state_params)

    def colour(self):
        return self.state.colour
