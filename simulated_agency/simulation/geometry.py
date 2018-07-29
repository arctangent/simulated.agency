
from functools import lru_cache as cache
from random import randint, shuffle

from ..location import Location


class Geometry(object):
    '''
    Provides simulation-level geometry
    '''

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

    @cache(maxsize=None)
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

    @cache(maxsize=None)
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
   
    @cache(maxsize=None)
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

    @cache(maxsize=None)
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

    def nearest(self, thing, candidates, radius=None):
        '''
        Returns the nearest of the candidates to thing.
        It would be very slow to check the distance to all things in
        the candidate_list, therefore we adopt a strategy of
        calculating what radius of neighbourhood gives us a reasonable
        chance of enclosing one of the things in the candidate list,
        and then widening our search radius if necessary.
        If radius is specified then this is taken as a fixed search
        radius and we do not widen our search beyond this.
        '''

        # User can pass an agent class or a list of agents
        if hasattr(candidates, 'objects'):
            candidate_list = candidates.objects
        else:
            candidate_list = candidates

        # Helper function to naively return nearest
        # from a list by brute force
        def nearest_brute_force(candidate_list):
            # If list is empty then return None
            if not candidate_list:
                return None
            # Shuffle because min always returns first item
            # in the set of all equally minimal items
            candidate_list = list(candidate_list)
            shuffle(candidate_list)
            return min(candidate_list, key=lambda x: thing.distance_to(x))
        
        if radius:
            # Use the supplied radius only
            neighbours = thing.location.neighbours(radius=radius)
            # Set intersection to find the ones we want
            catchment = set(candidate_list) & set(neighbours)
            return nearest_brute_force(catchment)

        # How sparsely populated are the candidates?
        density = len(candidate_list) / (self.simulation.width * self.simulation.height)

        # Calculate a reasonable starting search radius.
        # Note that the area covered scales with r^2 and so
        # the radius which gives us an expected catchment
        # of one thing is found by solving r^2 = 1 / density
        r = int(density ** -0.5)

        # If r is large then we might as well just brute force it
        if r > min(self.simulation.width, self.simulation.height) / 2:
            return nearest_brute_force(candidate_list)

        neighbours = thing.location.neighbours(radius=r)
        # Set intersection to find the ones we want
        catchment = set(candidate_list) & set(neighbours)
        
        # If we got at least one, then figure out the nearest
        if catchment:
            return nearest_brute_force(catchment)

        # None found in initial catchment area, so progressively
        # widen our search until we get something
        while True:
            r = r + 1
            neighbours = thing.location.neighbours(radius=r, border_only=True)
            # Set intersection to find the ones we want
            catchment = set(candidate_list) & set(neighbours)
            if catchment:
                break
        return nearest_brute_force(catchment)


    @cache(maxsize=None)
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

        if simulation.wrap_x:
            if dx > half_width:
                dx = dx - width
            elif -1 * dx > half_width:
                dx = dx + width     
        
        if simulation.wrap_y:
            if dy > half_height:
                dy = dy - height
            elif -1 * dy > half_height:
                dy = dy + height     

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

        # Since things may only move in four directions,
        # we must return the Manhattan distance
        return abs(dx) + abs(dy)
