
from .state import State


class MoveTowardsLocation(State):
    '''
    Represents moving towards a static location
    '''  

    name = 'MOVING_TOWARDS_LOCATION'
    colour = 9 #'red'
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
