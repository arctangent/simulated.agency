
import abc

from random import randint, choice

from .location import Location



class StateMachine(object):
    '''
    Manages states and transitions
    '''

    states = {}

    def __init__(self, states=[]):
        '''
        Init
        '''
        for state in states:
            self.register(state)

    def register(self, state):
        '''
        Add possible state to the machine
        '''
        self.states[state.name] = state

    def get_state_by_name(self, state_name):
        return self.states[state_name]

    def execute(self, agent):
        '''
        Run an agent through the state machine
        '''
        state_class = agent.state
        state_instance = state_class(agent)
        state_instance.execute(agent)


class State(abc.ABC):
    '''
    Abstract base class to define what a State is
    '''
    
    name = None
    colour = None
    timer = None
    required_params = []

    def __init__(self, agent, timer=None):
        if timer:
            self.timer = timer

    @abc.abstractmethod
    def execute(self, agent):
        # Check all required params are there
        if not all(key in agent.memory for key in self.required_params):
            raise Exception('Not all required params exist in agent memory')
        # Decrement timer if necessary
        if self.timer:
            self.timer -= 1
            if self.timer == 0:
                raise Exception('Now what do I do, Jacob?')
                # agent.set_state(agent.default_state)


class Dead(State):
    '''
    Represents death
    '''

    name = 'DEAD'
    colour = 'red'

    def execute(self, agent):
        super().execute(agent)
        pass


class Waiting(State):
    '''
    Represents waiting for some period of time
    '''

    name = 'WAITING'
    colour = 'cyan'
    required_params = []

    def execute(self, agent):
        super().execute(agent)


class MovingRandomly(State):
    '''
    Represents moving randomly
    ''' 

    name = 'MOVING_RANDOMLY'
    colour = 'green'

    def execute(self, agent):
        super().execute(agent)
        dice_roll = randint(1, 1000)
        if dice_roll == 1:
            agent.set_state(Dead)
        elif dice_roll <= 10:
            agent.set_state(Waiting, timer=randint(3,7))
        else:
            agent.move_randomly()
    

class MovingTowardsLocation(State):
    '''
    Represents moving towards a target location
    '''  

    name = 'MOVING_TOWARDS'
    colour = 'red'
    required_params = ['target_location']

    def execute(self, agent):
        super().execute(agent)
        target_location = agent.memory['target_location']
        agent.move_towards(target_location.x, target_location.y)
