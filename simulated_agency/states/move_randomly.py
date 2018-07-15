
from .state import State


class MoveRandomly(State):
    '''
    Represents moving randomly
    ''' 

    name = 'MOVING_RANDOMLY'
    colour = 'green'

    def handle(self):
        super().handle()
        self.agent.move_randomly()
