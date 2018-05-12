
from collections import defaultdict
    
class Location(object):
    '''
    Represents a location within the Simulation.
    '''

    simulation = None

    # Borg/Monostate pattern
    # Store instance state in class-level dict
    # indexed on (x, y) i.e. unique location identifier
    __shared_state = defaultdict(dict)
    
    def __init__(self, x, y, capacity=None):
        '''
        Initialise
        '''

        # Borg/Monostate pattern
        # If we already instantiated a location at (x, y)
        # then copy the state into the new location at (x, y)
        if (x, y) in Location.__shared_state.keys():
            self.__dict__ = Location.__shared_state[x, y]
            return

        #
        # Init code below runs only the first time a
        # location is instantiated at a particular (x, y)
        #
        
        # Ensure simulation is set
        assert self.simulation is not None, "Location must have 'simulation' property set!"
        
        # Basic properties
        self.x = x
        self.y = y
        
        # Location capacity
        # Setting this to zero effectively defines an impassable location
        self.capacity = capacity or 1

        # Contents
        self.contents = []
        
        # Pixel locations
        self.x_left = self.x * self.simulation.cell_size
        self.x_right = (self.x + 1) * self.simulation.cell_size
        self.y_top = self.y * self.simulation.cell_size
        self.y_bottom = (self.y + 1) * self.simulation.cell_size
        self.x_center = self.simulation.cell_size/2 + self.x_left
        self.y_center = self.simulation.cell_size/2 + self.y_top

        # Borg/Monostate pattern
        # The first time we instatiate a location at (x, y)
        # we must store that state in the class for later
        Location.__shared_state[x, y] = self.__dict__

    def __repr__(self):
        return 'Location (%s, %s) with contents %s' % (self.x, self.y, self.contents)

    def occupancy(self):
        '''
        Define this to be the number of agents in the location,
        i.e. no concept of 'mass' or 'size'.
        '''
        return len(self.contents)

    def is_full(self):
        return self.occupancy() == self.capacity

    def has_space(self):
        has_space = not self.is_full()
        return has_space
    
    def _wrap(self, val, min, max):
        '''
        Utility function to help with edge wrapping.
        '''
        
        if val < min:
            return 1 + max + val
        elif val > max:
            return val - max - 1
        else:
            return val
        
    def _wrap_width(self, val):
        '''
        Wrap a value within Simulation width
        '''

        if self.simulation.wrap_x:
            return self._wrap(val, 0, self.simulation.width - 1)
        else:
            if val < 0:
                return 0
            elif val > self.simulation.width - 1:
                return self.simulation.width - 1
            else:
                return val
    
    def _wrap_height(self, val):
        '''
        Wrap a value within Simulation height
        '''

        if self.simulation.wrap_y:
            return self._wrap(val, 0, self.simulation.height - 1)
        else:
            if val < 0:
                return 0
            elif val > self.simulation.height - 1:
                return self.simulation.height - 1
            else:
                return val
   
    #
    # Utility methods to make movement simpler to code.
    # Note that we memoise the locations so that we only
    # have to calculate them once.
    #
    
    _up = _down = _left = _right = None
    
    def up(self):
        if self._up:
            return self._up
        else:
            y = self._wrap_height(self.y - 1)
            self._up = Location(self.x, y)
            return self._up
    
    def down(self):
        if self._down:
            return self._down
        else:        
            y = self._wrap_height(self.y + 1)
            self._down = Location(self.x, y)
            return self._down
        
    def left(self):
        if self._left:
            return self._left
        else:    
            x = self._wrap_width(self.x - 1)
            self._left = Location(x, self.y)
            return self._left
    
    def right(self):
        if self._right:
            return self._right
        else:        
            x = self._wrap_width(self.x + 1)
            self._right = Location(x, self.y)
            return self._right

    def neighbours(self):
        return [self.up(), self.down(), self.left(), self.right()]