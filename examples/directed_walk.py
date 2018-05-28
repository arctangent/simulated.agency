
from random import randint

from simulated_agency.simulation import Simulation
from simulated_agency.agents import Mobile as Walker
from simulated_agency.states import *
 

# Initialise simulation
simulation = Simulation(cell_size=8, name='DirectedWalk')

# Bind models to simulation
Walker.simulation = simulation

# Create a target location
target_location = simulation.random_location()

# Add some walkers to the simulation
simulation.seed(Walker, 0.1, MoveToLocation, location=target_location)

# Define a function to run at the start of every loop.
# You only need to do this if you want to introduce
# some external change to the simulation (i.e. not
# governed by the States you have defined).
def maybe_move_target():
    ''' Change the target from time to time '''
    change_target = False
    target_location = None
    dice_roll = randint(1, 50)
    if dice_roll == 1:
        change_target = True
        target_location = simulation.random_location()
    # Very important to return any variables required by the
    # before_agent_run function. These must be in a dict.
    return {'change_target': change_target, 'target_location': target_location}

# Define a function to run on each agent before they execute and are drawn.
# You only need to do this if you have introduced external change as per
# the function defined above.
def update_agent(walker, maybe_move_target_return_vars):
    ''' Update agent target if the target location has changed '''
    # Use locals to access vars from maybe_move_target
    change_target = maybe_move_target_return_vars['change_target']
    target_location = maybe_move_target_return_vars['target_location']
    if change_target:
        walker.replace_state(MoveToLocation(walker, location=target_location))
            
# Run the simulation
simulation.execute(Walker, before_each_loop=maybe_move_target, before_each_agent=update_agent)

# Handle GUI events etc
simulation.window.mainloop()
