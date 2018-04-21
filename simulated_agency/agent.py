
from random import randint

from .location import Location


class AgentState(object):
    '''
    Represents the state of the Agent
    (This object resembles an Enum object)
    '''
        
    DEAD = 0
    WAITING = 1
    MOVING_RANDOMLY = 2
    MOVING_TOWARDS = 3
 
 
class Agent(object):
    '''
    Represents an agent that can move around in the World.
    '''
    
    world = None
        
    def __init__(self, location, state=None):
        '''
        Initialise
        '''
        
        # Ensure world is set
        assert self.world is not None, "Agent must have 'world' property set!"
        # Basic properties
        self.location = location
        # State - assumed to be random motion if not specified
        state = state or AgentState.MOVING_RANDOMLY
        self.set_state(state)
        
        
    def set_state(self, state, **kwargs):
        '''
        This function ensures that necessary initialisation
        actions are carried out when a Agent changes state.
        '''
        
        self.state = state
        
        # If state is WAITING then we need to set
        # a timer so that we know when to change states
        if self.state == AgentState.WAITING:
            self.timer = 10
            
        # If state is MOVING_TOWARDS then we need to ensure a target was specified
        if self.state == AgentState.MOVING_TOWARDS:
            if 'target' not in kwargs:
                raise Exception("No target specified!")
            else:
                self.target = kwargs['target']
        
    def colour(self):
        '''
        Returns the colour that a Agent should be drawn
        '''
        
        # Use different colours to show different states
        if self.state == AgentState.MOVING_RANDOMLY:
            return 'green'
        elif self.state == AgentState.DEAD:
            return 'red'
        elif self.state == AgentState.WAITING:
            return 'cyan'
        elif self.state == AgentState.MOVING_TOWARDS:
            return 'white'
        else:
            raise NotImplementedError
        
        
    def go(self):
        '''
        This method is called when it is a Agent's turn to do something.
        '''

        # Introduce a bit of randomness
        dice_roll = randint(1, 100)
        if dice_roll < 20:
            self.move_randomly()
        
        #
        # Based on current State, can/should we change State?
        #
        if self.state == AgentState.MOVING_RANDOMLY:
            # Maybe die, or perhaps take a shorter rest?
            dice_roll = randint(1, 100)
            if dice_roll == 1:
                self.set_state(AgentState.DEAD)
            elif dice_roll <= 10:
                self.set_state(AgentState.WAITING)
            else:
                self.move_randomly()
        elif self.state == AgentState.DEAD:
            # Dead Agents just remain where they are forever
            pass
        elif self.state == AgentState.WAITING:
            # Decrement our timer
            self.timer -= 1
            # Can we change state?
            if self.timer == 0:
                self.set_state(AgentState.MOVING_RANDOMLY)
        elif self.state == AgentState.MOVING_TOWARDS:
            # Move towards the target
            # We need to check whether the target
            # *has* a location or *is* a location
            if isinstance(self.target, Location):
                self.move_towards(self.target.x, self.target.y)
            elif hasattr(self.target, 'location'):
                self.move_towards(self.target.location.x, self.target.location.y)
            else:
                raise NotImplementedError("Unable to move towards this object")
        else:
            raise NotImplementedError("No action for state provided")
    
                                              
    def move_towards(self, target_x, target_y):
        '''
        Move stochstically in the direction of the target.
        '''
        
        # Compute naive, non-wrapping distance
        dx = target_x - self.location.x
        dy = target_y - self.location.y
        
        # Adjust for screen wrap
        # Note that dx and dy could be negative
        if self.world.wrap_x:
            if abs(dx) > (self.world.width / 2):
                dx = ((dx + (self.world.width * 3/2)) % self.world.width) - (self.world.width / 2)
        if self.world.wrap_y:
            if abs(dy) > (self.world.height / 2):
                dy = ((dy + (self.world.height * 3/2)) % self.world.height) - (self.world.height / 2)

        # Decide which direction to move in depending
        # on the magnituds of the component parts of the vector
        if dx == dy == 0:
            # We're at the location
            pass
        elif dx == 0:
            # Move in direction of dy
            if dy > 0:
                self.move_to_location(self.location.down())
            else:
                self.move_to_location(self.location.up())
        elif dy == 0:
            # Move in direction of dx
            if dx > 0:
                self.move_to_location(self.location.right())
            else:
                self.move_to_location(self.location.left())
        else:
            # Decide stochastically which direction to move in
            dx2 = dx * dx
            dy2 = dy * dy
            hypotenuse2 = dx2 + dy2
            dice_roll = randint(1, hypotenuse2)
            if dice_roll <= dx2:
                # Move in direction of dx
                if dx > 0:
                    self.move_to_location(self.location.right())
                else:
                    self.move_to_location(self.location.left())
            else:
                # Move in direction of dy
                if dy > 0:
                    self.move_to_location(self.location.down())
                else:
                    self.move_to_location(self.location.up())
            
        
            
    def move_randomly(self):
        '''
        Move the Agent in a random direction.
        '''
        
        # Randomly choose from up/down/left/right
        move_choice = randint(1, 4)
        if move_choice == 1:
            self.move_to_location(self.location.up())
        elif move_choice == 2:
            self.move_to_location(self.location.down())
        elif move_choice == 3:
            self.move_to_location(self.location.left())
        else:
            self.move_to_location(self.location.right())
    
    
    def move_to_location(self, new_loc):
        '''
        Move the Agent to a directly adjacent location.
        '''

        new_location = self.world.locations[new_loc.x, new_loc.y]
        
        # Check that proposed new location is not full to capacity
        if new_location.is_full():
            # Do nothing
            return
        
        # Remove from current location
        current_location = self.world.locations[self.location.x, self.location.y]
        current_location.contents.remove(self)
        
        # Add to new location
        self.location = new_location
        new_location.contents.append(self)
