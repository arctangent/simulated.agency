
from random import randint
from time import time

RECORD_VIDEO = False
START_TIME = time()

SKETCH_WIDTH = 1600
SKETCH_HEIGHT = 800
CELL_SIZE = 80          

WORLD_WIDTH = SKETCH_WIDTH / CELL_SIZE
WORLD_HEIGHT = SKETCH_HEIGHT / CELL_SIZE

NUM_WALKERS = 50

BACKGROUND_COLOUR = 0


    
 
        
    
class Walker(object):
    
    world = None
    
    def __init__(self, location):
        # Ensure world is set
        assert self.world is not None, "Walker must have 'world' property set!"
        # Basic properties
        self.location = location
        
    def draw(self):
        fill(200, 0, 0)
        rectMode(CENTER)
        rect(self.location.x_center, self.location.y_center, CELL_SIZE, CELL_SIZE)
        
    def move(self):
        self.move_randomly()
        # Don't forget to draw self
        self.draw()
                
    def move_randomly(self):
        # Randomly choose from up/down/left/right
        move_choice = randint(1, 4)
        if move_choice == 1:
            self.move_to_location(self.location.up())
        elif move_choice == 2:
            self.move_to_location(self.location.down())
        elif move_choice == 3:
            self.move_to_location(self.location.left())
        else:
            self.move_to_location(self.location.right())
    
    def move_to_location(self, new_location):
        # Check that proposed new location is empty
        if self.world.locations[new_location.x, new_location.y].contents is not None:
            # Do nothing
            return
        # Remove from current location
        self.world.locations[self.location.x, self.location.y].unset()
        # Add to new location
        self.location = self.world.locations[new_location.x, new_location.y]
        self.world.locations[new_location.x, new_location.y].contents = self        

    
class Location(object):
    
    world = None
    
    def __init__(self, x, y):
        # Ensure world is set
        assert self.world is not None, "Location must have 'world' property set!"
        # Basic properties
        self.x = x
        self.y = y
        # Start empty
        self.contents = None
        # Pixel locations
        self.x_center = CELL_SIZE/2 + self.x * CELL_SIZE
        self.y_center = CELL_SIZE/2 + self.y * CELL_SIZE
    
    def unset(self):
        self.contents = None
        fill(BACKGROUND_COLOUR)
        rectMode(CENTER)
        rect(self.x_center, self.y_center, CELL_SIZE, CELL_SIZE)
        
    def _wrap(self, val, min, max):
        if val < min:
            return 1 + max + val
        elif val > max:
            return val - max - 1
        else:
            return val
        
    def up(self):
        y = self._wrap(self.y - 1, 0, self.world.height - 1)
        return self.world.locations[self.x, y]
    
    def down(self):
        y = self._wrap(self.y + 1, 0, self.world.height - 1)
        return self.world.locations[self.x, y]
    
    def left(self):        
        x = self._wrap(self.x - 1, 0, self.world.width - 1)
        return self.world.locations[x, self.y]
    
    def right(self):        
        x = self._wrap(self.x + 1, 0, self.world.width - 1)
        return self.world.locations[x, self.y]
    

    
class World(object):
    
    locations = {}
    things = []
    
    def __init__(self, world_width, world_height):
        # Basic properties
        self.width = world_width
        self.height = world_height

        
        


def setup():
    frameRate(15)
    
    # Initialise output window
    size(SKETCH_WIDTH, SKETCH_HEIGHT)
    
    # Initialise world
    global world
    world = World(WORLD_WIDTH, WORLD_HEIGHT)
    
    # Add some locations to the world - specifically, a simple grid
    Location.world = world
    for x in xrange(0, world.width):
        for y in xrange(0, world.height):
            world.locations[x, y] = Location(x, y)
            
    # Add some walkers to the world
    Walker.world = world
    for _ in xrange(0, NUM_WALKERS):
        x = randint(0, world.width - 1)
        y = randint(0, world.height -1)
        walker = Walker(world.locations[x, y])
        world.locations[x, y].contents = walker
        world.things.append(walker)
        
    # Initial screen draw
    background(BACKGROUND_COLOUR)
    noStroke()
    for thing in world.things:
        thing.draw()
    

def draw():
    # Go through the list of things and move them one by one
    for thing in world.things:
        thing.move()
    if RECORD_VIDEO:
        saveFrame("images/random-walk-" + str(START_TIME) + "-######.png")
        
        
def keyPressed():
    saveFrame("images/random-walk-######.png")
