
    
class Location(object):
    '''
    Represents a location within the World.
    '''
    
    world = None
    
    def __init__(self, x, y, capacity=None):
        '''
        Initialise
        '''
        
        # Ensure world is set
        assert self.world is not None, "Location must have 'world' property set!"
        
        # Basic properties
        self.x = x
        self.y = y
        
        # Location capacity
        # Setting this to zero effectively defines an impassable location
        if capacity is None:
            capacity = 1
        self.capacity = capacity

        # Contents
        self.contents = []
        
        # Pixel locations
        self.x_left = self.x * self.world.cell_size
        self.x_right = (self.x + 1) * self.world.cell_size
        self.y_top = self.y * self.world.cell_size
        self.y_bottom = (self.y + 1) * self.world.cell_size
        self.x_center = self.world.cell_size/2 + self.x_left
        self.y_center = self.world.cell_size/2 + self.y_top
     
    def occupancy(self):
        '''
        Define this to be the number of agents in the location,
        i.e. no concept of 'mass' or 'size'.
        '''
        return len(self.contents)

    def is_full(self):
        return self.occupancy() == self.capacity
     
    
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
        Wrap a value within World width
        '''

        if self.world.wrap_x:
            return self._wrap(val, 0, self.world.width - 1)
        else:
            if val < 0:
                return 0
            elif val > self.world.width - 1:
                return self.world.width - 1
            else:
                return val
    
    def _wrap_height(self, val):
        '''
        Wrap a value within World height
        '''

        if self.world.wrap_y:
            return self._wrap(val, 0, self.world.height - 1)
        else:
            if val < 0:
                return 0
            elif val > self.world.height - 1:
                return self.world.height - 1
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
            self._up = self.world.locations[self.x, y]
            return self._up
    
    def down(self):
        if self._down:
            return self._down
        else:        
            y = self._wrap_height(self.y + 1)
            self._down = self.world.locations[self.x, y]
            return self._down
        
    def left(self):
        if self._left:
            return self._left
        else:    
            x = self._wrap_width(self.x - 1)
            self._left = self.world.locations[x, self.y]
            return self._left
    
    def right(self):
        if self._right:
            return self._right
        else:        
            x = self._wrap_width(self.x + 1)
            self._right = self.world.locations[x, self.y]
            return self._right
    
