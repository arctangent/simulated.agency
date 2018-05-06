
from random import randint

from .location import Location
from .mixins import Mobile

from .states import Dead, Waiting, MovingRandomly, MovingTowards


class Agent(Mobile):
    '''
    Represents an agent that can move around in the World.
    '''
    
    world = None
        
    def __init__(self, location=None, state=None):
        '''
        Initialise
        '''
        super().__init__(location, state)
        # Ensure world is set
        assert self.world is not None, "Agent must have 'world' property set!"

        # State - assumed to be random motion if not specified
        state = state or MovingRandomly
        self.set_state(state)
        
        
    def set_state(self, state, **kwargs):
        '''
        This function ensures that necessary initialisation
        actions are carried out when an Agent changes state.
        '''
        
        # We pass the kwargs to the state class so it can init correctly
        self.state = state(self, **kwargs)
