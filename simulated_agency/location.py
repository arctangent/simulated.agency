
from collections import defaultdict
    
class Location(object):
    '''
    Represents a location within the Simulation.
    '''
    
    simulation = None
    colour = None
    
    def __init__(self, x, y, capacity=None):
        '''
        Initialise
        '''
        
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

        # Memoised results
        self._up = self._down = self._left = self._right = None
        self._neighbours = None
        self._neighbourhood = None

    def __repr__(self):
        return 'Location(%s, %s)' % (self.x, self.y)

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
    
    def up(self):
        if self._up:
            return self._up
        else:
            y = self._wrap_height(self.y - 1)
            self._up = self.simulation.locations[self.x, y]
            return self._up
    
    def down(self):
        if self._down:
            return self._down
        else:        
            y = self._wrap_height(self.y + 1)
            self._down = self.simulation.locations[self.x, y]
            return self._down
        
    def left(self):
        if self._left:
            return self._left
        else:    
            x = self._wrap_width(self.x - 1)
            self._left = self.simulation.locations[x, self.y]
            return self._left
    
    def right(self):
        if self._right:
            return self._right
        else:        
            x = self._wrap_width(self.x + 1)
            self._right = self.simulation.locations[x, self.y]
            return self._right

    #
    # Definition of neighbours and neighbourhoods
    #

    def neighbours(self, include_self=False, include_self_location=False, recalculate=False):
        '''
        Returns the neighbours of a given cell.
        This is a aggregate list of the contents of its neighbourhood, less itself.
        Note that this will include any other agents in the same location as us.
        '''

        if self._neighbours and not recalculate:
            return self._neighbours
        
        neighbours_list = [
            neighbour
            for cell in self.neighbourhood(include_self_location=include_self_location)
            for neighbour in cell.contents
        ]

        if not include_self and include_self_location:
            neighbours_list.remove(self)
        
        self._neighbours = neighbours_list

        return neighbours_list

    def neighbourhood(self, include_self_location=True, recalculate=False):
        '''
        Returns the neighbourhood of a given cell.
        This can be calculated in several ways.
        '''

        if self._neighbourhood and not recalculate:
            return self._neighbourhood
        
        # Strategy pattern
        strategy = self.simulation.neighbourhood_strategy

        if strategy == 'von_neumann':
            # Von Neumann neighbourhood is the cell itself and the four adjacent cells
            neighbourhood_list = [self, self.up(), self.down(), self.left(), self.right()]
        elif strategy == 'moore':
            # Moore neighbourhood is the cell itself and the eight cells surrounding it
            neighbourhood_list =  [
                self.up().left(), self.up(), self.up().right(),
                self.left(), self, self.right(),
                self.down().left(), self.down(),  self.down().right()
            ]

        if not include_self_location:
            neighbourhood_list.remove(self)

        self._neighbourhood = neighbourhood_list

        return neighbourhood_list
