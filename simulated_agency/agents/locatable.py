
from .stateful import *


class Locatable(Stateful):
    '''
    Represents a type of agent which has a location.
    '''

    mass = 1

    def __new__(cls, initial_location, initial_state=None, **kwargs):
        # We should only create an instance of a thing
        # if the specified location has room for it
        if not initial_location.can_fit(cls):
            return None

        instance = super().__new__(cls)
        return instance

    def __init__(self, initial_location, initial_state=None, **kwargs):
        super().__init__(initial_state, **kwargs)     
        self.location = initial_location
        self.location.contents.append(self)

    def __repr__(self):
        return 'Locatable %s at (%s, %s)' % (self._state_stack.peek(), self.location.x, self.location.y)
        
    def destroy(self):
        # The object may have been destroyed already
        # this turn, so we proceed carefully
        try:
            self.location.contents.remove(self)
        except:
            pass
        # We need to delete the object last
        super().destroy()

    #
    # Distance functions
    #

    def vector_to(self, target_x, target_y):
        ''' Returns a screen wrapping-aware shortest vector to target
        '''
        return self.simulation.vector_between(self.location.x, self.location.y, target_x, target_y)

    def distance_to(self, other):
        ''' Returns a screen wrapping-aware distance
        '''
        return self.simulation.distance_between(self, other)

    def nearest(self, candidate_list, radius=None):
        ''' Returns the nearest of the candidates
        '''
        return self.simulation.nearest(self, candidate_list, radius=radius)
