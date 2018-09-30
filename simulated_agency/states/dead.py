
from .state import State


class Dead(State):
    '''
    Represents death
    '''

    name = 'DEAD'
    colour = (255, 0, 0)
    glyph = 'X'

    def handle(self):
        super().handle()
