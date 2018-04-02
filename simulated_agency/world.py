


class World(object):
    '''
    Represents the universe in which our simulation unfolds.
    '''
    
    def __init__(self, world_width, world_height, cell_size):    
        # Basic properties
        self.width = world_width
        self.height = world_height
        self.cell_size = cell_size
        self.locations = {}
        self.things = []