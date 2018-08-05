
import sys

from random import randint, choice, shuffle
from time import time
from tkinter import *

from ..location import Location
from .executor import *
from .geometry import *
from .seeder import *


class Simulation(object):
    '''
    Represents the universe in which our simulation unfolds.
    '''

    # Strategy pattern for neighbour location
    neighbourhood_strategy = 'von_neumann'
    
    def __init__(self, width=None, height=None, name=None):

        # Name of this simulation - used for file output
        self.name = name or 'simulation'

        # Locations
        self.locations = {}

        # Bound agent classes
        self.bound_agent_classes = []

        # Constants - do not change these directly after simulation instantiation
        self.width = width or 80
        self.height = height or 40
        self.background_colour = 0 #'black'
        
        # Computed properties
        self.init_locations()

        # Preferences
        self.record_video = False

        # Wrapping
        self.wrap_x = True
        self.wrap_y = True

        # Track simulation age
        self.age = 0

        # Delegate functionality - bind methods
        Seeder(self)
        Geometry(self)
        Executor(self)

    def init_locations(self):
        Location.simulation = self
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.locations[x, y] = Location(x, y)

    def bind(self, *args):
        '''
        Agent classes should be bound to the simulation using this method

        e.g. simulation.bind(Wolves, Sheep)
        '''

        for agent_class in args:
            if agent_class not in self.bound_agent_classes:
                # Add to the list of bound agent classes
                self.bound_agent_classes.append(agent_class)
                # Bind the class to the simulation
                agent_class.simulation = self
