
from collections import defaultdict
from functools import lru_cache as cache
    
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
    
    @cache(maxsize=None)
    def up(self):
        y = self.simulation.normalise_height(self.y - 1)
        return self.simulation.locations[self.x, y]
    
    @cache(maxsize=None)
    def down(self):
        y = self.simulation.normalise_height(self.y + 1)
        return self.simulation.locations[self.x, y]

    @cache(maxsize=None)    
    def left(self):
        x = self.simulation.normalise_width(self.x - 1)
        return self.simulation.locations[x, self.y]
    
    @cache(maxsize=None)
    def right(self):   
        x = self.simulation.normalise_width(self.x + 1)
        return self.simulation.locations[x, self.y]

    #
    # Definition of neighbours and neighbourhoods
    #

    def neighbours(self, radius=1, include_self=False, include_self_location=False):
        '''
        Returns the neighbours of a given cell.
        This is a aggregate list of the contents of its neighbourhood, less itself.
        Note that this will include any other agents in the same location as us.
        '''
    
        neighbours_list = [
            neighbour
            for cell in self.neighbourhood(radius=radius, include_self_location=include_self_location)
            for neighbour in cell.contents
        ]

        if not include_self and include_self_location:
            neighbours_list.remove(self)

        return neighbours_list

    @cache(maxsize=None)
    def neighbourhood(self, radius=1, border_only=False, include_self_location=True):
        '''
        Returns a set containing the neighbourhood of a given cell.
        This can be calculated in several ways.
        If border_only is True then only the edge is returned,
        allowing us to progressively explore a wider radius.
        '''

        # Sanity check
        if (radius < 1) or (int(radius) != radius):
            raise Exception("Radius must be a positive integer")
        
        # Strategy pattern
        strategy = self.simulation.neighbourhood_strategy

        # Helper function to define condtion for inclusion
        # in the neighbourhood set
        def include(dx, dy):
            if strategy == 'von_neumann':
                # Von Neumann neighbourhood for r==1 is
                # the cell itself and the four adjacent cells
                if border_only:
                    return abs(dx) + abs(dy) == radius
                else:
                    return abs(dx) + abs(dy) <= radius
            elif strategy == 'moore':
                # Moore neighbourhood for r==1 is
                # the cell itself and the eight cells surrounding it
                if border_only:
                    return (abs(dx) == radius) or (abs(dy) == radius)
                else:
                    return True
                
        # Build the neighbourhood set

        neighbourhood_set = set()
            
        for dx in range(-1 * radius, radius + 1):
            for dy in range(-1 * radius, radius + 1):
                if include(dx, dy):
                    x = self.simulation.normalise_width(self.x + dx)
                    y = self.simulation.normalise_height(self.y + dy)
                    neighbourhood_set.add(self.simulation.locations[x, y])

        if not include_self_location:
            neighbourhood_set.remove(self)

        return neighbourhood_set

    #
    # Distance functions
    #

    def vector_to(self, target_x, target_y):
        ''' Returns a screen wrapping-aware shortest vector to target
        '''
        return self.simulation.vector_between(self.x, self.y, target_x, target_y)

    def distance_to(self, other):
        ''' Returns a screen wrapping-aware distance
        '''
        return self.simulation.distance_between(self, other)

    def nearest(self, candidate_list):
        ''' Returns the nearest of the candidates
        '''
        return self.simulation.nearest(self, candidate_list)
