
from random import randint, shuffle

from ..location import Location


class Geometry(object):
    '''
    Provides simulation-level geometry
    '''

    # Memoisation
    # Note that we are happy to share these dicts with any child classes
    # (unlike the "objects" attribute of Stateful)
    wrapped_dx = {}
    wrapped_dy = {}
    distances = {}

    def __init__(self, simulation):
        self.simulation = simulation
        # Bind methods
        self.simulation.normalise_width = self.normalise_width
        self.simulation.normalise_height = self.normalise_height
        self.simulation.random_x = self.random_x
        self.simulation.random_y = self.random_y
        self.simulation.random_xy = self.random_xy
        self.simulation.random_location = self.random_location
        self.simulation.nearest = self.nearest
        self.simulation.vector_between = self.vector_between
        self.simulation.distance_between = self.distance_between

    #
    # Internal methods
    #

    def _wrap(self, val, min_val, max_val):
        '''
        Utility function to help with wrapping edges.
        '''
        
        if val < min_val:
            return 1 + max_val + val
        elif val > max_val:
            return val - max_val - 1
        else:
            return val

    def _constrain(self, val, min_val, max_val):
        '''
        Utility function to help with non-wrapping edges.
        '''

        if val < min_val:
            return min_val
        elif val > max_val:
            return max_val
        else:
            return val

    #
    # Normalisation
    #
   
    def normalise_width(self, val):
        '''
        Ensure a value remains within Simulation width
        either by wrapping or constraining
        '''

        simulation = self.simulation

        if simulation.wrap_x:
            # Wrap
            return self._wrap(val, 0, simulation.width - 1)
        else:
            # Constrain
            return self._constrain(val, 0, simulation.width - 1)

    def normalise_height(self, val):
        '''
        Ensure a value remains within Simulation height
        either by wrapping or constraining
        '''

        simulation = self.simulation

        if simulation.wrap_y:
            # Wrap
            return self._wrap(val, 0, simulation.height - 1)
        else:
            # Constrain
            return self._constrain(val, 0, simulation.height - 1)

    #
    # Random coordinates
    #

    def random_x(self):
        return randint(0, self.simulation.width - 1)

    def random_y(self):
        return randint(0, self.simulation.height - 1)

    def random_xy(self):
        return self.random_x(), self.random_y()

    def random_location(self):
        return self.simulation.locations[self.random_xy()]

    #
    # Distances
    #

    def nearest(self, thing, candidate_list):
        '''
        Returns the nearest of the candidates to thing
        '''

        # Shuffle because min always returns first item
        # in the set of all equally minimal items
        shuffle(candidate_list)
        return min(candidate_list, key=lambda x: thing.distance_to(x))

    def vector_between(self, x1, y1, x2, y2):
        '''
        Returns a screen wrapping-aware shortest vector
        between (x1, y1) and (x2, y2)
        '''

        # Shorthand references
        simulation = self.simulation
        width = simulation.width
        height = simulation.height
        half_width = width / 2
        half_height = height / 2

        # Compute naive, non-wrapping distance
        dx = x2 - x1
        dy = y2 - y1

        # Adjust for screen wrap
        # We memoise these calculations for speed

        try:
            dx = self.wrapped_dx[dx] 
        except:
            if not simulation.wrap_x:
                self.wrapped_dx[dx] = dx
            else:
                new_dx = dx
                if dx > half_width:
                    new_dx = dx - width
                elif -1 * dx > half_width:
                    new_dx = dx + width
                self.wrapped_dx[dx] = new_dx        
                dx = new_dx
        
        try:
            dy = self.wrapped_dy[dy]
        except:
            if not simulation.wrap_y:
                self.wrapped_dy[dy] = dy
            else:
                new_dy = dy
                if dy > half_height:
                    new_dy = dy - height
                elif -1 * dy > half_height:
                    new_dy = dy + height
                self.wrapped_dy[dy] = new_dy        
                dy = new_dy

        # Return the vector components
        return dx, dy

    def distance_between(self, thing1, thing2):
        '''
        Returns a screen wrapping-aware distance
        '''

        # Things must be a location or have a location

        if isinstance(thing1, Location):
            x1 = thing1.x
            y1 = thing1.y
        elif hasattr(thing1, 'location'):
            x1 = thing1.location.x
            y1 = thing1.location.y
        else:
            raise Exception('Cannot calculate distance from unlocatable object') 

        if isinstance(thing2, Location):
            x2 = thing2.x
            y2 = thing2.y
        elif hasattr(thing2, 'location'):
            x2 = thing2.location.x
            y2 = thing2.location.y
        else:
            raise Exception('Cannot calculate distance to unlocatable object') 

        # Get vector between things
        dx, dy = self.vector_between(x1, y1, x2, y2)

        # Memoisation
        try:
            distance = self.distances[x1, y1, x2, y2]
        except:
            distance = (dx**2 + dy**2)**0.5
            self.distances[x1, y1, x2, y2] = distance

        return distance
