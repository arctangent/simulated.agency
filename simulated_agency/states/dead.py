
from .state import State


class Dead(State):
    '''
    Represents death
    '''

    name = 'DEAD'
    colour = 'red'
    glyph = 'X'

    def handle(self):
        super().handle()
