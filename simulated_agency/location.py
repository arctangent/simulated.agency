
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

    def mass(self):
        '''
        How much mass is concentrated in this location?
        '''
        return sum([ a.mass for a in self.contents ])

    def can_fit(self, other):
        '''
        Can some other thing fit in this location?
        '''
        return (self.mass() + other.mass <= self.capacity)

    #
    # Utility methods to make movement simpler to code.
    # Note that we memoise the locations so that we only
    # have to calculate them once.
    #
    
    def up(self):
        if self._up:
            return self._up
        else:
            y = self.simulation.normalise_height(self.y - 1)
            self._up = self.simulation.locations[self.x, y]
            return self._up
    
    def down(self):
        if self._down:
            return self._down
        else:        
            y = self.simulation.normalise_height(self.y + 1)
            self._down = self.simulation.locations[self.x, y]
            return self._down
        
    def left(self):
        if self._left:
            return self._left
        else:    
            x = self.simulation.normalise_width(self.x - 1)
            self._left = self.simulation.locations[x, self.y]
            return self._left
    
    def right(self):
        if self._right:
            return self._right
        else:        
            x = self.simulation.normalise_width(self.x + 1)
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
        Returns a set containing the neighbourhood of a given cell.
        This can be calculated in several ways.
        '''

        if self._neighbourhood and not recalculate:
            return self._neighbourhood
        
        # Strategy pattern
        strategy = self.simulation.neighbourhood_strategy

        if strategy == 'von_neumann':
            # Von Neumann neighbourhood is the cell itself and the four adjacent cells
            neighbourhood_set = { self, self.up(), self.down(), self.left(), self.right() }
        elif strategy == 'moore':
            # Moore neighbourhood is the cell itself and the eight cells surrounding it
            neighbourhood_set =  {
                self.up().left(), self.up(), self.up().right(),
                self.left(), self, self.right(),
                self.down().left(), self.down(),  self.down().right()
            }

        if not include_self_location:
            neighbourhood_set.remove(self)

        self._neighbourhood = neighbourhood_set

        return neighbourhood_set
