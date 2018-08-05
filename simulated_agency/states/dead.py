
from .state import State


class Dead(State):
    '''
    Represents death
    '''

    name = 'DEAD'
    colour = 9 #'red'
    glyph = 'X'

    def handle(self):
        super().handle()
