
from collections import defaultdict
from random import choice, randint

from ..states import State, MoveRandomly
from .locatable import *


class Mobile(Locatable):
    '''
    Represents a type of agent which can change its location.
    '''

    # Memoisation
    # Note that we are happy to share these dicts with any child classes
    # (unlike the "objects" attribute of Stateful)
    wrapped_dx = {}
    wrapped_dy = {}

    def __init__(self, initial_location, initial_state=None, **kwargs):
        super().__init__(initial_location, initial_state, **kwargs)

    def __repr__(self):
        return 'Mobile with state %s at (%s, %s)' % (self._state_stack.peek(), self.location.x, self.location.y)

    def move_to_location(self, new_loc):
        '''
        Move the agent to a specified adjacent location.
        '''
        
        new_location = self.simulation.locations[new_loc.x, new_loc.y]
        
        # Check that proposed new location is not full to capacity
        if new_location.is_full():
            # Do nothing
            return
        
        # Remove from current location
        self.location.contents.remove(self)

        # Add to new location
        self.location = new_location
        new_location.contents.append(self)

    def move_randomly(self):
        location = choice(self.location.neighbourhood())
        self.move_to_location(location)

    def move_towards_location(self, location):
        self.move_towards(location.x, location.y)

    def move_towards_target(self, target):
        self.move_towards(target.location.x, target.location.y)

    def move_away_from_target(self, target):
        '''
        Move in a direction that prevents the target being
        able to move into you next turn.
        '''
        location = self.location
        allowed_moves = [location.up(), location.down(), location.left(), location.right()]

        # We use a 'knockout' technique to find the safe locations.
        # Example: An enemy in any square above us means that we do
        # not want to move upwards. Similarly with the other directions

        if target.location in [location.up(), location.up().left(), location.up().right()]:
            allowed_moves.remove(location.up())
        elif target.location in [location.down(), location.down().left(), location.down().right()]:
            allowed_moves.remove(location.down())
        elif target.location in [location.left(), location.left().up(), location.left().down()]:
            allowed_moves.remove(location.left())
        elif target.location in [location.right(), location.right().up(), location.right().down()]:
            allowed_moves.remove(location.right())

        # Choose randomly from what's left
        new_location = choice(allowed_moves)
        self.move_to_location(new_location)
            

    def move_towards(self, target_x, target_y):
        '''
        Move stochstically in the direction of the target coordinates
        '''

        # Shorthand references
        simulation = self.simulation
        width = simulation.width
        height = simulation.height
        half_width = width / 2
        half_height = height / 2

        # Compute naive, non-wrapping distance
        dx = target_x - self.location.x
        dy = target_y - self.location.y
        
        # Adjust for screen wrap
        # We memoise these calculations for speed

        try:
            dx = self.wrapped_dx[dx] 
        except:
            if not simulation.wrap_x:
                self.wrapped_dx[dx] = dx
            else:
                new_dx = dx
                if dx > half_width:
                    new_dx = dx - width
                elif -1 * dx > half_width:
                    new_dx = dx + width
                self.wrapped_dx[dx] = new_dx        
                dx = new_dx
        
        try:
            dy = self.wrapped_dy[dy]
        except:
            if not simulation.wrap_y:
                self.wrapped_dy[dy] = dy
            else:
                new_dy = dy
                if dy > half_height:
                    new_dy = dy - height
                elif -1 * dy > half_height:
                    new_dy = dy + height
                self.wrapped_dy[dy] = new_dy        
                dy = new_dy


        # Decide which direction to move in depending
        # on the magnitudes of the component parts of the vector
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
