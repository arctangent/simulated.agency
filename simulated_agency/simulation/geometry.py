
from random import randint


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


    def random_x(self):
        return randint(0, self.simulation.width - 1)

    def random_y(self):
        return randint(0, self.simulation.height - 1)

    def random_xy(self):
        return self.random_x(), self.random_y()

    def random_location(self):
        return self.simulation.locations[self.random_xy()]
