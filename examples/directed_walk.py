
from random import randint, choice


# Ugly hack to fix s.a imports
import sys
sys.path.append(sys.path[0] + "/..")
sys.path.append(sys.path[0] + "/../..")

from simulated_agency.world import World
from simulated_agency.location import Location
from simulated_agency.agent import Agent, AgentState
 


# Constants
NUM_WALKERS = 500

# Initialise world
world = World()

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
            


while True:
    '''
    Event loop
    '''

    # Counter for image frame numbers
    world.counter += 1
    
    # Clear the canvas
    world.canvas.delete('all')

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
        world.draw(thing.location.x, thing.location.y, fill=thing.colour())

    # Draw the target last
    target_gui_handle = world.canvas.find_withtag('target')
    world.draw(target_x, target_y, fill='red')

    # Update the canvas
    world.canvas.after(20)
    world.canvas.update()

    # Save images
    if world.record_video:
        world.save_image('images/directed_walk/')
        

world.window.mainloop()