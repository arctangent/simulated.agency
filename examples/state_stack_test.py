
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

# Constants
NUM_WALKERS = int(simulation.width * simulation.height * 0.1)

# Create a target location
target_location = simulation.random_location()

# Add some walkers to the simulation
for _ in range(0, NUM_WALKERS):
    # Try to add - may fail if location already occupied
    w = ForgetfulWalker(simulation.random_location())
    if w:
        w.add_state(MoveRandomly(w))
        w.add_state(MoveToLocation(w, location=target_location, timer=randint(10,30)))
            


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