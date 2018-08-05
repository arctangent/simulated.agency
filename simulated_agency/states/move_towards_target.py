
from .state import State


class MoveTowardsTarget(State):
    '''
    Represents moving towards a mobile target
    '''
    
    name = 'MOVING_TOWARDS_TARGET'
    colour = 9 #'red'
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
