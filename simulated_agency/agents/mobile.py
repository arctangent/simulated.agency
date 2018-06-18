
from collections import defaultdict
from random import choice, choices, randint

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
        Internal method to perform a known-successful relocation.
        Use move_to_location instead of calling this directly.
        '''
        # Remove from current location
        self.location.contents.remove(self)
        # Add to new location
        self.location = new_location
        new_location.contents.append(self)

    def move_to_location(self, new_location, alt_moves=[], alt_moves_final=[]):
        '''
        Move the agent to a specified location,
        substituting alt_moves if they are specified and valid
        '''

        if new_location.can_fit(self):
            # Perform the relocation
            self._relocate(new_location)

        # Were any alternative moves supplied?
        # We allow None to be specified, which indicates a choice to stay in current location
        if alt_moves:
            viable_alt_moves = [alt for alt in alt_moves if alt is None or alt.can_fit(self)]
            if viable_alt_moves:
                new_location = choice(viable_alt_moves)
            elif alt_moves_final:
                # Select from the moves of last resort
                viable_alt_moves_final = [alt for alt in alt_moves_final if alt is None or alt.can_fit(self)]
                if viable_alt_moves_final:
                    new_location = choice(viable_alt_moves_final)
            # None means stay put
            if new_location is not None:
                self._relocate(new_location)

    def move_towards_location(self, location):
        self.move_towards(location.x, location.y)

    def move_towards_target(self, target):
        self.move_towards(target.location.x, target.location.y)

    def move_randomly(self):
        location = choice(tuple(self.location.neighbourhood()))
        self.move_towards_location(location)

    def move_away_from_target(self, target):
        '''
        Move in a direction that prevents the target being
        able to move into you next turn.
        '''

        # Shorthand references
        up = self.location.up()
        down = self.location.down()
        left = self.location.left()
        right = self.location.right()
        location = self.location

        # We use a 'knockout' technique to find the safe locations.
        # Example: An enemy in any square above us means that we do
        # not want to move upwards. Similarly with the other directions

        allowed_moves = [up, down, left, right]

        if target.location in [up, up.left(), up.right()]:
            allowed_moves.remove(up)
        elif target.location in [down, down.left(), down.right()]:
            allowed_moves.remove(down)
        elif target.location in [left, left.up(), left.down()]:
            allowed_moves.remove(left)
        elif target.location in [right, right.up(), right.down()]:
            allowed_moves.remove(right)

        # Choose randomly from what's left
        new_location = choice(allowed_moves)
        self.move_towards_location(new_location)
            

    def move_towards(self, target_x, target_y):
        '''
        Move stochstically in the direction of the target coordinates
        '''

        # Compute naive, non-wrapping distance
        dx = target_x - self.location.x
        dy = target_y - self.location.y

        # Exit early if we are at the location
        if dx == dy == 0:
            return

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

        #
        # Decide which direction to move in depending
        # on the magnitudes of the component parts of the vector
        #

        choices(
            [ self.move_horizontal(dx, dy), self.move_vertical(dx, dy) ],
            weights=[abs(dx), abs(dy)]    
        )  

    def move_horizontal(self, dx, dy):
        '''
        Move in direction of dx,
        picking alt_moves based on dy
        '''

        # Shorthand references
        move = self.move_to_location
        up = self.location.up()
        down = self.location.down()
        left = self.location.left()
        right = self.location.right()

        if dx > 0:
            # Try to move right...
            if dy > 0:
                # ... with second preference for moving down
                move(right, alt_moves=[down], alt_moves_final=[up, None])
            elif dy < 0:
                # ... with second preference for moving up
                move(right, alt_moves=[up], alt_moves_final=[down, None])
            else:
                # ... with second preference for moving up/down
                move(right, alt_moves=[up, down, None])
        else:
            # Try to move left...
            if dy > 0:
                # ... with second preference for moving down
                move(left, alt_moves=[down], alt_moves_final=[up, None])
            elif dy < 0:
                # ... with second preference for moving up
                move(left, alt_moves=[up], alt_moves_final=[down, None])
            else:
                # ... with second preference for moving up/down
                move(left, alt_moves=[up, down, None])

    def move_vertical(self, dx, dy):
        '''
        Move in direction of dy,
        picking alt_moves based on dx
        '''
        
        # Shorthand references
        move = self.move_to_location
        up = self.location.up()
        down = self.location.down()
        left = self.location.left()
        right = self.location.right()

        if dy > 0:
            # Try to move down...
            if dx > 0:
                # ... with second preference for moving right
                move(down, alt_moves=[right], alt_moves_final=[left, None])
            elif dx < 0:
                # ... with second preference for moving left
                move(down, alt_moves=[left], alt_moves_final=[right, None])
            else:
                # ... with second preference for moving left/right
                move(down, alt_moves=[left, right, None])
        else:
            # Try to move up...
            if dx > 0:
                # ... with second preference for moving right
                move(up, alt_moves=[right], alt_moves_final=[left, None])
            elif dx < 0:
                # ... with second preference for moving left
                move(up, alt_moves=[left], alt_moves_final=[right, None])
            else:
                # ... with second preference for moving left/right
                move(up, alt_moves=[left, right, None])        
