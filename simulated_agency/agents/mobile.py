
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

    def _relocate(self, new_location):
        '''
        Internal method to perform a known-successfuk relocation.
        Use move_to_location instead of calling this directly.
        '''
        # Remove from current location
        self.location.contents.remove(self)
        # Add to new location
        self.location = new_location
        new_location.contents.append(self)

    def move_to_location(self, new_location, alternatives=[]):
        '''
        Move the agent to a specified location
        '''
        
        # If we cannot move to the proposed new location
        # then we try to find a sensible alternative
        if not new_location.can_fit(self):
            # Were any alternative moves supplied?
            if alternatives:
                viable_alternatives = [alt for alt in alternatives if alt.can_fit(self)]
                if viable_alternatives:
                    new_location = choice(viable_alternatives)
                    self._relocate(new_location)
                else:
                    # None of the specified alternatives
                    # was available, so do nothing
                    pass

            # No alternatives specified, so we will do the best we can.
            # Identify which axis we were trying to move on
            if self.location.x - new_location.x == 0:
                # Can't move up/down, but maybe left or right would work?
                left = new_location.left()
                right = new_location.right()
                left_available = left.can_fit(self)
                right_available = right.can_fit(self)
                # Determine alternative location
                if left_available and right_available:
                    new_location = choice([self.location.left(), self.location.right()])
                elif left_available:
                    new_location = self.location.left()
                elif right_available:
                    new_location = self.location.right()
                else:
                    # We failed to find an alternative, so do nothing
                    return
            else:
                # Attempted an left/right move
                # Can't move left/right, but maybe up or down would work?
                up = new_location.up()
                down = new_location.down()
                up_available = up.can_fit(self)
                down_available = down.can_fit(self)
                # Determine alternative location
                if up_available and down_available:
                    new_location = choice([self.location.up(), self.location.down()])
                elif up_available:
                    new_location = self.location.up()
                elif down_available:
                    new_location = self.location.down()
                else:
                    # We failed to find an alternative, so do nothing
                    return 
        
        # Perform the relocation
        self._relocate(new_location)

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
        move = self.move_to_location
        up = self.location.up()
        down = self.location.down()
        left = self.location.left()
        right = self.location.right()

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
                move(down)
            else:
                move(up)
        elif dy == 0:
            # Move in direction of dx
            if dx > 0:
                move(right)
            else:
                move(left)
        else:
            # Decide stochastically which direction to move in
            abs_dx = abs(dx)
            abs_dy = abs(dy)
            distance = abs_dx + abs_dy
            # Determine the direction to move
            dice_roll = randint(1, distance)
            if dice_roll <= abs_dx:
                # Move in direction of dx
                if dx > 0:
                    if dy > 0:
                        move(right, alternatives=[down])
                    elif dy < 0:
                        move(right, alternatives=[up])
                    else:
                        move(right)
                else:
                    if dy > 0:
                        move(left, alternatives=[down])
                    elif dy < 0:
                        move(left, alternatives=[up])
                    else:
                        move(left)
            else:
                # Move in direction of dy
                if dy > 0:
                    if dx > 0:
                        move(down, alternatives=[right])
                    elif dx < 0:
                        move(down, alternatives=[left])
                    else:
                        move(down)
                else:
                    if dx > 0:
                        move(up, alternatives=[right])
                    elif dx < 0:
                        move(up, alternatives=[left])
                    else:
                        move(up)
