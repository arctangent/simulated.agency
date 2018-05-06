
import abc

from random import randint

from .location import Location


class State(abc.ABC):
    '''
    Abstract base class to define what a State is
    '''

    def __init__(self, agent=None):
        self.agent = agent

    @abc.abstractmethod
    def execute(self, agent):
        pass


class Dead(State):
    '''
    Represents death
    '''

    def __init__(self, agent):
        super().__init__(agent)
        self.name = 'DEAD'
        self.colour = 'red'

    def execute(self):
        pass


class Waiting(State):
    '''
    Represents waiting for some period of time
    '''

    def __init__(self, agent, timer=None):
        super().__init__(agent)
        self.name = 'WAITING'
        self.colour = 'cyan'
        self.timer = timer or randint(10, 100)

    def execute(self):
        self.timer -= 1
        if self.timer == 0:
            self.agent.set_state(MovingRandomly)


class MovingRandomly(State):
    '''
    Represents moving randomly
    ''' 

    def __init__(self, agent):
        super().__init__(agent)
        self.name = 'MOVING_RANDOMLY'
        self.colour = 'green'

    def execute(self):
        agent = self.agent
        dice_roll = randint(1, 1000)
        if dice_roll == 1:
            agent.set_state(Dead)
        elif dice_roll <= 10:
            agent.set_state(Waiting)
        else:
            self.move_randomly()
    
    def move_randomly(self):
        # Randomly choose from up/down/left/right
        agent = self.agent
        move_choice = randint(1, 4)
        if move_choice == 1:
            agent.move_to_location(agent.location.up())
        elif move_choice == 2:
            agent.move_to_location(agent.location.down())
        elif move_choice == 3:
            agent.move_to_location(agent.location.left())
        else:
            agent.move_to_location(agent.location.right())        


class MovingTowards(State):
    '''
    Represents moving towards a target
    '''  

    def __init__(self, agent, target=None):
        super().__init__(agent)
        self.name = 'DEAD'
        self.colour = 'red'
        if target is None:
            raise Exception("No target specified!")
        else:
            self.target = target

    def execute(self):
        # We need to check whether the target
        # *has* a location or *is* a location
        if isinstance(self.target, Location):
            self.move_towards(self.target.x, self.target.y)
        elif hasattr(self.target, 'location'):
            self.move_towards(self.target.location.x, self.target.location.y)
        else:
            raise NotImplementedError("Unable to move towards this object")

    def move_towards(self, target_x, target_y):
        '''
        Move stochstically in the direction of the target.
        '''

        # Shorthand references
        agent = self.agent
        world = agent.world

        # Compute naive, non-wrapping distance
        dx = target_x - agent.location.x
        dy = target_y - agent.location.y
        
        # Adjust for screen wrap
        # Note that dx and dy could be negative
        if world.wrap_x:
            if abs(dx) > (world.width / 2):
                dx = ((dx + (world.width * 3/2)) % world.width) - (world.width / 2)
        if world.wrap_y:
            if abs(dy) > (world.height / 2):
                dy = ((dy + (world.height * 3/2)) % world.height) - (world.height / 2)

        # Decide which direction to move in depending
        # on the magnituds of the component parts of the vector
        if dx == dy == 0:
            # We're at the location
            pass
        elif dx == 0:
            # Move in direction of dy
            if dy > 0:
                agent.move_to_location(agent.location.down())
            else:
                agent.move_to_location(agent.location.up())
        elif dy == 0:
            # Move in direction of dx
            if dx > 0:
                agent.move_to_location(agent.location.right())
            else:
                agent.move_to_location(agent.location.left())
        else:
            # Decide stochastically which direction to move in
            dx2 = dx * dx
            dy2 = dy * dy
            hypotenuse2 = dx2 + dy2
            dice_roll = randint(1, hypotenuse2)
            if dice_roll <= dx2:
                # Move in direction of dx
                if dx > 0:
                    agent.move_to_location(agent.location.right())
                else:
                    agent.move_to_location(agent.location.left())
            else:
                # Move in direction of dy
                if dy > 0:
                    agent.move_to_location(agent.location.down())
                else:
                    agent.move_to_location(agent.location.up())
 
