
    
class Location(object):
    '''
    Represents a location within the World.
    '''
    
    world = None
    
    def __init__(self, x, y):
        '''
        Initialise
        '''
        
        # Ensure world is set
        assert self.world is not None, "Location must have 'world' property set!"
        
        # Basic properties
        self.x = x
        self.y = y
        
        # Start empty
        self.contents = None
        
        # Pixel locations
        self.x_left = self.x * self.world.cell_size
        self.x_right = (self.x + 1) * self.world.cell_size
        self.y_top = self.y * self.world.cell_size
        self.y_bottom = (self.y + 1) * self.world.cell_size
        self.x_center = self.world.cell_size/2 + self.x_left
        self.y_center = self.world.cell_size/2 + self.y_top
     
           
    def unset(self):
        '''
        Remove contents from location and redraw it as empty.
        '''
        
        self.contents = None
    
    
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
        return self._wrap(val, 0, self.world.width - 1)
    
    def _wrap_height(self, val):
        '''
        Wrap a value within World height
        '''
        return self._wrap(val, 0, self.world.height - 1)
   
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
    
