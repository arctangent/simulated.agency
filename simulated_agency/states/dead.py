
from .state import State


class Dead(State):
    '''
    Represents death
    '''

    name = 'DEAD'
    colour = 'red'
    glyph = 'X'
    size = 0.75

    def handle(self):
        super().handle()
