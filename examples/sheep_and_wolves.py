
from random import choice

from simulated_agency.simulation import Simulation
from simulated_agency.agents import Mobile
from simulated_agency.states import *


class KillTarget(State):
    '''
    Agents in this state will kill a target
    if it is adjacent to them, otherwise they will
    do nothing and proceed to the next state.
    '''

    name = 'DESTROY_TARGET'
    colour = 'red'
    required_params = ['target']

    def handle(self):
        target = self.context['target']
        if target in self.agent.location.neighbours():
            target.replace_state(Dead)
        self.agent.remove_state()


class ChooseTargetToFollow(State):
    '''
    Agents in this state will choose a target
    to follow and then begin following it.

    Note that due to the design of the MoveTowardsTarget
    state, they will return to this state after getting
    close to their target and thus choose another one.
    '''

    name = 'CHOOSE_TARGET_TO_FOLLOW'
    colour = 'yellow'
    required_params = ['prey']

    def handle(self):
        target_list = self.context['prey'].objects
        # Wolves will only chase Sheep that are alive
        live_target_list = [x for x in target_list if not x.is_in_state(Dead)]
        # Choose target
        if live_target_list:
            # Choose the nearest live target
            target = self.agent.nearest(live_target_list)
            # Assign the state
            # When we have done moving towards the target we will kill it
            self.agent.add_state(KillTarget, target=target)
            # Remember, the last state added is the first to execute
            self.agent.add_state(MoveTowardsTarget, target=target)
        else:
            # No sheep left to chase
            self.agent.add_state(MoveRandomly)

# Initialise simulation
simulation = Simulation(cell_size=8, name='SheepAndWolves')

# Use same base model for two types of object
class Sheep(Mobile): pass
class Wolves(Mobile): pass

# Bind models to simulation
simulation.bind(Wolves, Sheep)

# Add some sheep to the simulation
simulation.seed(Sheep, 0.15, AvoidType, enemy=Wolves, comfort_zone=3)

# Add some wolves to the simulation
simulation.seed(Wolves, 50, ChooseTargetToFollow, prey=Sheep)

# Run the simulation
simulation.execute(draw_locations=False)
