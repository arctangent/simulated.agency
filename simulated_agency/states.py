
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
        
        state_class = self.get_state_by_name(agent.state_name)
        state = state_class()
        state.execute(agent)


class State(abc.ABC):
    '''
    Abstract base class to define what a State is
    '''
    
    name = None
    colour = None

    @abc.abstractmethod
    def execute(self, agent):
        pass


class Dead(State):
    '''
    Represents death
    '''

    name = 'DEAD'
    colour = 'red'

    def execute(self, agent):
        pass


class Waiting(State):
    '''
    Represents waiting for some period of time
    '''

    name = 'WAITING'
    colour = 'cyan'
    required_params = ['timer']

    def execute(self, agent):
        agent.memory['timer'] -= 1
        if agent.memory['timer'] == 0:
            agent.set_state(MovingRandomly)


class MovingRandomly(State):
    '''
    Represents moving randomly
    ''' 

    name = 'MOVING_RANDOMLY'
    colour = 'green'

    def execute(self, agent):
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
        target_location = agent.memory['target_location']
        agent.move_towards(target_location.x, target_location.y)
