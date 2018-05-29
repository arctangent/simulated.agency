
from random import choice, choices

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
            target.replace_state(Dead(target))
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
    required_params = ['target_list']

    def handle(self):
        target_list = self.context['target_list']
        # Choose target
        while True:
            # Ensure we choose a live target
            target = choice(target_list)
            if not target.is_in_state(Dead):
                # FIXME: All wolves chase the same sheep!
                print('Wolf %s chooses Sheep %s' % (id(self.agent), id(target)))
                break
        # Assign the state
        # When we have done moving towards the target we will kill it
        self.agent.add_state(KillTarget(self.agent, target=target))
        # Remember, the last state added is the first to execute
        self.agent.add_state(MoveTowardsTarget(self.agent, target=target))


# Initialise simulation
simulation = Simulation(cell_size=20, name='Following')

# Use same base model for two types of object
class Sheep(Mobile): pass
class Wolves(Mobile): pass

# Bind models to simulation
Sheep.simulation = simulation
Wolves.simulation = simulation

# Add some sheep to the simulation
simulation.seed(Sheep, 100, MoveRandomly)

# Add some wolves to the simulation
simulation.seed(Wolves, 5, ChooseTargetToFollow, target_list=Sheep.objects)

# Run the simulation
simulation.execute([Wolves, Sheep])

# Handle GUI events etc
simulation.window.mainloop()
