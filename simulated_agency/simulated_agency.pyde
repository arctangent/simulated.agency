
from random import randint


from constants import *
from world import World
from location import Location
from walker import Walker, WalkerState






        
#
# Below here is code specific to Processing
# to initialise our objects and to get the
# event loop started.
#        


def setup():
    '''
    Set up the Processing sketch
    '''
    
    # Set simulation frame rate
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
    
    # Specify the World the Walkers live in
    Walker.world = world
    
    # Specify an initial target
    target_x = world.width / 4
    target_y = world.height / 4
    global target
    target = world.locations[target_x, target_y]   
    
    # Add some walkers to the world
    for _ in xrange(0, NUM_WALKERS):
        x = randint(0, world.width - 1)
        y = randint(0, world.height -1)
        walker = Walker(world.locations[x, y])
        world.locations[x, y].contents = walker
        walker.set_state(WalkerState.MOVING_TOWARDS, target=target)
        world.things.append(walker)
               
    # Initial screen draw
    background(BACKGROUND_COLOUR)
    noStroke()
    for thing in world.things:
        thing.draw()
    

def draw():
    '''
    Code to be run each time Processing's event loop is executed.
    '''
    
    global target
    
    # Change the target from time to time
    change_target = False
    dice_roll = randint(1, 50)
    if dice_roll == 1:
        change_target = True
        target.unset()
        target_x = randint(0, world.width - 1)
        target_y = randint(0, world.height - 1)
        target = world.locations[target_x, target_y]
    
    # Go through the list of things and tell each of them to do something
    for thing in world.things:
        if change_target:
            thing.set_state(WalkerState.MOVING_TOWARDS, target=target)
        # Tell the thing to act
        thing.do_something()
        
    # Draw the target
    fill(255, 0, 0)
    rectMode(CENTER)
    rect(target.x_center, target.y_center, CELL_SIZE, CELL_SIZE)   

                            
    if RECORD_VIDEO:
        saveFrame("images/random-walk-" + str(START_TIME) + "-######.png")
        

def mouseClicked():
    setup()
    
def keyPressed():
    '''
    If the user presses a key then take a screenshot.
    '''
    
    saveFrame("images/######.png")