
from constants import *


class World(object):
    '''
    Represents the universe in which our simulation unfolds.
    '''
    
    def __init__(self, world_width, world_height):    
        # Basic properties
        self.width = world_width
        self.height = world_height
        self.locations = {}
        self.things = []