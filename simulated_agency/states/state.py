
import abc

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
    size = 2

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
