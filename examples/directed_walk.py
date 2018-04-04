
from random import randint, choice
from time import time
from tkinter import *

# Linux doesn't have ImageGrab but we can use pyscreenshot instead
try:
    from PIL import ImageGrab
except:
    import pyscreenshot as ImageGrab

# Ugly hack to fix s.a imports
import sys
sys.path.append(sys.path[0] + "/..")
sys.path.append(sys.path[0] + "/../..")

from simulated_agency.world import World
from simulated_agency.location import Location
from simulated_agency.agent import Agent, AgentState



# Constants
# FIXME: These should be attributes of the World

RECORD_VIDEO = False
START_TIME = time()

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800
CELL_SIZE = 8       

WORLD_WIDTH = int(CANVAS_WIDTH / CELL_SIZE)
WORLD_HEIGHT = int(CANVAS_HEIGHT / CELL_SIZE)

NUM_WALKERS = 500

BACKGROUND_COLOUR = 0


# Set up GUI
window = Tk()
window.resizable(False, False)
canvas = Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='black', bd=0, highlightthickness=0)
canvas.pack()

# Initialise counter for image frame numbers
counter = 0
    
# Initialise world
world = World(WORLD_WIDTH, WORLD_HEIGHT, CELL_SIZE)

# Add some locations to the world - specifically, a simple grid
Location.world = world
for x in range(0, world.width):
    for y in range(0, world.height):
        world.locations[x, y] = Location(x, y)

# A Walker is identical to the Agent class (for now)
Walker = Agent

# Specify the World the Walkers live in
Walker.world = world

# Specify an initial target
target_x = int(world.width / 4)
target_y = int(world.height / 4)
target = world.locations[target_x, target_y]

# Add some walkers to the world
for _ in range(0, NUM_WALKERS):
    x = randint(0, world.width - 1)
    y = randint(0, world.height -1)
    walker = Walker(world.locations[x, y])
    world.locations[x, y].contents = walker
    walker.set_state(AgentState.MOVING_TOWARDS, target=target)
    world.things.append(walker)
            
# Convenient draw function
def rect(x, y, fill):
    if CELL_SIZE < 4:
        width = 0
    else:
        width = int(CELL_SIZE / 5)
    canvas.create_rectangle(CELL_SIZE * x, CELL_SIZE * y, CELL_SIZE * (x + 1), CELL_SIZE * (y + 1), fill=fill, width=width)

while True:
    '''
    Event loop
    '''

    # Counter for image frame numbers
    counter += 1
    
    # Clear the canvas
    canvas.delete('all')

    # Change the target from time to time
    change_target = False
    dice_roll = randint(1, 30)
    if dice_roll == 1:
        change_target = True
        target.unset()
        target_x = randint(0, world.width - 1)
        target_y = randint(0, world.height - 1)
        target = world.locations[target_x, target_y]
    
    # Go through the list of things and tell each of them to do something
    for thing in world.things:
        if change_target:
            thing.set_state(AgentState.MOVING_TOWARDS, target=target)
        # Tell the thing to act
        thing.do_something()
        rect(thing.location.x, thing.location.y, fill=thing.colour())

    # Draw the target last
    target_gui_handle = canvas.find_withtag('target')
    rect(target_x, target_y, fill='red')

    # Update the canvas
    canvas.after(20)
    canvas.update()

    # Save images
    if RECORD_VIDEO:
        # The name of our image
        image_name = 'images/directed_walk/' + str(counter).zfill(8) + '.png'

        # Compute location of screen to grab
        x1 = window.winfo_rootx() + canvas.winfo_x()
        y1 = window.winfo_rooty() + canvas.winfo_y()
        x2 = x1 + canvas.winfo_width()
        y2 = y1 + canvas.winfo_height()
        
        # Save the image
        ImageGrab.grab((x1, y1, x2, y2)).save(image_name)


window.mainloop()