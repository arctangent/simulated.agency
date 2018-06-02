
import abc

from random import randint, choice

from simulated_agency import glyphs

class State(abc.ABC):
    '''
    Abstract base class to define what a State is
    '''
    
    name = None
    colour = None
    timer = None
    required_params = []
    # Used for drawing
    glyph = glyphs.BLACK_SQUARE
    size = 1

    def __init__(self, agent, **kwargs):
        self.agent = agent
        # Track state age (i.e. how long in this state)
        self.age = 0
        # Set countdown if specified
        if 'timer' in kwargs.keys():
            self.timer = kwargs['timer']
        # Check all required data is there
        if not all(key in kwargs for key in self.required_params):
            raise Exception('Not all required data exist in state context')
        # Update state context
        self.context = {}
        self.context.update(**kwargs)

    def __repr__(self):
        return 'State(%s)' % self.name

    @abc.abstractmethod
    def handle(self):
        ''' Execute the state in it's context '''
        # Increment state age
        self.age += 1
        # Decrement timer if necessary
        if self.timer:
            self.timer -= 1
            if self.timer == 0:
                self.handle_timeout()
                
    def handle_timeout(self):
        ''' Called by default when the timer hits zero '''
        # Stop doing the thing we're doing
        self.agent.remove_state()


class Dead(State):
    '''
    Represents death
    '''

    name = 'DEAD'
    colour = 'red'
    glyph = 'X'

    def handle(self):
        super().handle()


class Wait(State):
    '''
    Represents waiting for some period of time
    '''

    name = 'WAITING'
    colour = 'cyan'
    required_params = ['timer']

    def handle(self):
        super().handle()


class MoveRandomly(State):
    '''
    Represents moving randomly
    ''' 

    name = 'MOVING_RANDOMLY'
    colour = 'green'

    def handle(self):
        super().handle()
        self.agent.move_randomly()
    

class MoveTowardsLocation(State):
    '''
    Represents moving towards a static location
    '''  

    name = 'MOVING_TOWARDS_LOCATION'
    colour = 'red'
    required_params = ['location']

    def handle(self):
        super().handle()
        # Are we "there" yet? (There = in the location)
        location = self.context['location']
        if self.agent.location == location:
            # When we arrive, we do the next thing
            # in the state stack
            self.agent.remove_state()
            return
        # Move towards location
        self.agent.move_towards_location(location)
        

class MoveTowardsTarget(State):
    '''
    Represents moving towards a mobile target
    '''
    
    name = 'MOVING_TOWARDS_TARGET'
    colour = 'red'
    required_params = ['target']

    def handle(self):
        super().handle()
        # Are we "there" yet? (There = adjacent to the target)
        target = self.context['target']
        if target in self.agent.location.neighbours():
            # When we arrive, we do the next thing
            # in the state stack
            self.agent.remove_state()
            return
        # Move towards target
        self.agent.move_towards_target(target)


class AvoidType(State):
    '''
    Avoid all members of a particular class.
    Example: sheep.add_state(AvoidType, enemy=Wolves)

    FIXME: For simplicity we just pick one neighbouring
           enemy and try to avoid only it
    '''

    name = 'AVOID_TYPE'
    colour = 'green'
    required_params = ['enemy']

    def handle(self):
        super().handle()
        # Is there a member of the specified class nearby?
        enemy_type = self.context['enemy']
        agent = self.agent
        location = agent.location
        # Enumerate neighbouring enemies
        enemies = [x for x in location.neighbours() if type(x) is enemy_type]
        if enemies:
            # Choose one to avoid
            enemy_to_avoid = choice(enemies)
            agent.move_away_from_target(enemy_to_avoid)
        else:
            agent.move_randomly()
