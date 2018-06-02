
from .stateful import *


class Locatable(Stateful):
    '''
    Represents a type of agent which has a location.
    '''

    def __new__(cls, initial_location, initial_state=None, **kwargs):
        # We should only create an instance of a thing
        # if the specified location has room for it
        if initial_location.is_full():
            return None

        instance = super().__new__(cls)
        return instance

    def __init__(self, initial_location, initial_state=None, **kwargs):
        super().__init__(initial_location, initial_state, **kwargs)      
        self.location = initial_location
        self.location.contents.append(self)

    def __repr__(self):
        return 'Locatable %s at (%s, %s)' % (self._state_stack.peek(), self.location.x, self.location.y)
        
    def destroy(self):
        # The object may have been destroyed already
        # this turn, so we proceed carefully
        try:
            self.location.contents.remove(self)
            self.simulation.canvas.delete(self.canvas_id)
        except:
            pass
        # We need to delete the object last
        super().destroy()
     