
from random import randint

from simulated_agency.simulation import Simulation
from simulated_agency.agents import Mobile as ForgetfulWalker
from simulated_agency.states import *
 

# Initialise simulation
simulation = Simulation(cell_size=8, name='ForgetfulWalk')

# Bind models to simulation
ForgetfulWalker.simulation = simulation

# Create a target location
target_location = simulation.random_location()

# Add some walkers to the simulation
simulation.seed(ForgetfulWalker, 0.1, MoveTowardsLocation, location=target_location, timer=randint(10,30))

# Define a function to run at the start of every loop.
# You only need to do this if you want to introduce
# some external change to the simulation (i.e. not
# governed by the States you have defined).
def maybe_move_target():
    ''' Change the target from time to time '''
    change_target = False
    target_location = None
    dice_roll = randint(1, 100)
    if dice_roll == 1:
        change_target = True
        target_location = simulation.random_location()
    # Very important to return any variables required by the
    # before_agent_run function. These must be in a dict.
    return {'change_target': change_target, 'target_location': target_location}

# Define a function to run on each agent before they execute and are drawn.
# You only need to do this if you have introduced external change as per
# the function defined above.
def update_agent_target(walker, maybe_move_target_return_vars):
    ''' Update agent target if the target location has changed '''
    # Use locals to access vars from maybe_move_target
    change_target = maybe_move_target_return_vars['change_target']
    target_location = maybe_move_target_return_vars['target_location']
    if change_target:
        walker.flush_state_stack()
        # Note that stack is populated from bottom to top, so the next three lines
        # instruct a walker to (1) Wait a short while, (2) MoveTowardsLocation for a while,
        # and then (3) forget what they are doing and MoveRandomly (until this code
        # branch is executed again by the target changing).
        walker.add_state(MoveRandomly)
        walker.add_state(MoveTowardsLocation, location=target_location, timer=randint(10,30))
        walker.add_state(Wait, timer=randint(1, 10))

# Run the simulation
simulation.execute(ForgetfulWalker, before_each_loop=maybe_move_target, before_each_agent=update_agent_target, draw_locations=False)

# Handle GUI events etc
simulation.window.mainloop()
