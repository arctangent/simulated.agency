
from .state import State


class AvoidType(State):
    '''
    Avoid all members of a particular class.
    Example: sheep.add_state(AvoidType, enemy=Wolves)

    FIXME: For simplicity we just pick the nearest enemy
           and take evasive action if it comes too close
    '''

    name = 'AVOID_TYPE'
    colour = 10 #'green'
    required_params = ['enemy', 'comfort_zone']

    def handle(self):
        super().handle()
        enemy = self.context['enemy']
        comfort_zone = self.context['comfort_zone']
        agent = self.agent
        nearest_enemy = agent.nearest(enemy.objects)
        # Only trigger avoidance within the comfort zone
        if agent.distance_to(nearest_enemy) <= comfort_zone:
            agent.move_away_from_target(nearest_enemy)
        else:
            # Do nothing
            pass
