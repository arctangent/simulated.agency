
from random import randint, choice
from tkinter import *

from constants import *
from world import World
from location import Location
from walker import Walker, WalkerState

# ImageGrab doesn't work on Linux
try:
    from PIL import ImageGrab
except:
    RECORD_VIDEO = False



# Set up GUI
window = Tk()
window.resizable(False, False)
canvas = Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='black', bd=0, highlightthickness=0)
canvas.pack()

# Initialise counter for image frame numbers
counter = 0
    
# Initialise world
world = World(WORLD_WIDTH, WORLD_HEIGHT)

# Add some locations to the world - specifically, a simple grid
Location.world = world
for x in range(0, world.width):
    for y in range(0, world.height):
        world.locations[x, y] = Location(x, y)

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
    walker.set_state(WalkerState.MOVING_TOWARDS, target=target)
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
        image_name = 'images/' + str(counter).zfill(8) + '.png'

        # Compute location of screen to grab
        x1 = window.winfo_rootx() + canvas.winfo_x()
        y1 = window.winfo_rooty() + canvas.winfo_y()
        x2 = x1 + canvas.winfo_width()
        y2 = y1 + canvas.winfo_height()
        
        # Save the image
        ImageGrab.grab((x1, y1, x2, y2)).save(image_name)


window.mainloop()
