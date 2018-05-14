
from random import randint, choice, shuffle


# Ugly hack to fix s.a imports
import sys
sys.path.append(sys.path[0] + "/..")
sys.path.append(sys.path[0] + "/../..")

from simulated_agency.simulation import Simulation
from simulated_agency.location import Location
from simulated_agency.agents import Agent as ForgetfulWalker
from simulated_agency.states import *
 

# Initialise simulation
simulation = Simulation(cell_size=8)
Location.simulation = simulation
ForgetfulWalker.simulation = simulation

# Create a target location
target_location = simulation.random_location()

# Add some walkers to the simulation
simulation.seed(ForgetfulWalker, 0.1, MoveToLocation, location=target_location, timer=randint(10,30))
            


def loop():
    '''
    Event loop
    '''

    # Counter for image frame numbers
    simulation.counter += 1
    
    # Clear the canvas
    simulation.canvas.delete('all')

    # Change the target location from time to time
    change_target = False
    dice_roll = randint(1, 100)
    if dice_roll == 1:
        change_target = True
        target_location = simulation.random_location()
    
    # Go through the list of agents and tell each of them to do something
    shuffle(ForgetfulWalker.objects)
    for w in ForgetfulWalker.objects:
        if change_target:
            w.flush_state_stack()
            # Note that stack is populated from bottom to top, so the next three lines
            # instruct a walker to (1) Wait a short while, (2) MoveToLocation for a while,
            # and then (3) forget what they are doing and MoveRandomly (until this code
            # branch is executed again by the target changing).
            w.add_state(MoveRandomly(w))
            w.add_state(MoveToLocation(w, location=target_location, timer=randint(10,30)))
            w.add_state(Wait(w, timer=randint(1, 10)))
        # Tell the agent to act
        w.execute()
        simulation.draw(w)

    # Save images
    if simulation.record_video:
        simulation.save_image('directed_walk')

    simulation.canvas.after(20, loop)
        
loop()
simulation.window.mainloop()