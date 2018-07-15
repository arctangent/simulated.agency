
from .state import State


class Wait(State):
    '''
    Represents waiting for some period of time
    '''

    name = 'WAITING'
    colour = 'cyan'
    required_params = ['timer']

    def handle(self):
        super().handle()
