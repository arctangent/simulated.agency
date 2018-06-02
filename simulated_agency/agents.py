
from collections import defaultdict
from random import choice, randint

from .states import State, MoveRandomly


class Stack(object):
    '''
    Represents a stack of states
    '''

    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

    def flush(self):
        self.items = []


class HasOwnObjectList(type):
    '''
    Metaclass to ensure that each class derived from
    the Stateful class has it's own copy of an
    `objects` list. Otherwise the derived classes would
    share the same list, which isn't what you'd want.

    Example:
        class Sheep(Mobile): pass
        class Wolves(Mobile): pass

    Now when you create Sheep they appear in Sheep.objects but
    they do not appear in Wolves.objects, as you would expect.    
    '''

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls.objects = []


class Stateful(object, metaclass=HasOwnObjectList):
    '''
    Represents something which can be created and destroyed,
    and which can also have a state and transition between states.
    '''

    simulation = None
    # Used for drawing
    size = 1

    def __init__(self, initial_location, initial_state=None, **kwargs):
        # Ensure simulation is set
        assert self.simulation is not None, "Creatable objects must have 'simulation' property set!"
        # Track agent age
        self.age = 0
        # Init
        self.objects.append(self)
        self._state_stack = Stack()
        # Default state
        self.default_state = MoveRandomly
        # Initial state
        if initial_state:
            self.add_state(initial_state, **kwargs)

    def destroy(self):
        # The object may have been destroyed already
        # this turn, so we proceed carefully
        try:
            self.objects.remove(self)
            del self
        except:
            pass

    def execute(self):
        if self._state_stack.is_empty():
            self._state_stack.push(self.default_state)
        # Delegate to state machine
        self._state_stack.peek().handle()

    def is_in_state(self, state_class):
        return isinstance(self.current_state_instance(), state_class)

    def current_state_instance(self):
        ''' Return the top entry of the state stack '''
        return self._state_stack.peek()

    def current_state_class(self):
        ''' Return the class of the top entry of the state stack '''
        return self.current_state_instance().__class__

    def replace_state(self, state_class, **kwargs):
        ''' Replace the top entry of the state stack with a new state '''
        state_instance = state_class(self, **kwargs)
        if self._state_stack.size():
            self._state_stack.pop()
        self._state_stack.push(state_instance)

    def replace_state_instance(self, state_instance):
        ''' Replace the top entry of the state stack with a new state '''
        if self._state_stack.size():
            self._state_stack.pop()
        self._state_stack.push(state_instance)

    def add_state(self, state_class, **kwargs):
        ''' Change state by addind a new state to the state stack '''
        state_instance = state_class(self, **kwargs)
        self._state_stack.push(state_instance)

    def remove_state(self):
        ''' Change state by removing the top state from the stack '''
        self._state_stack.pop()
        # Ensure there's always something in the state stack
        if self._state_stack.is_empty():
            self.add_state(self.default_state)

    def flush_state_stack(self):
        ''' Remove all states and replace with default state '''
        self._state_stack.flush()
        self._state_stack.push(self.default_state)

    def colour(self):
        return self._state_stack.peek().colour


class Locatable(Stateful):
    '''
    Represents a type of agent which has a location.
    '''

    def __new__(cls, initial_location, initial_state=None, **kwargs):
        # We should only create an instance of a thing
        # if the specified location has room for it
        if initial_location.is_full():
            return None

        instance = super().__new__(cls)
        return instance

    def __init__(self, initial_location, initial_state=None, **kwargs):
        super().__init__(initial_location, initial_state, **kwargs)      
        self.location = initial_location
        self.location.contents.append(self)

    def __repr__(self):
        return 'Locatable %s at (%s, %s)' % (self._state_stack.peek(), self.location.x, self.location.y)
        
    def destroy(self):
        # The object may have been destroyed already
        # this turn, so we proceed carefully
        try:
            self.location.contents.remove(self)
        except:
            pass
        # We need to delete the object last
        super().destroy()
     

class Mobile(Locatable):
    '''
    Represents a type of agent which can change its location.
    '''

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

        # Compute naive, non-wrapping distance
        dx = target_x - self.location.x
        dy = target_y - self.location.y
        
        # Adjust for screen wrap
        # Note that dx and dy could be negative
        if simulation.wrap_x:
            if abs(dx) > (simulation.width / 2):
                dx = ((dx + (simulation.width * 3/2)) % simulation.width) - (simulation.width / 2)
        if simulation.wrap_y:
            if abs(dy) > (simulation.height / 2):
                dy = ((dy + (simulation.height * 3/2)) % simulation.height) - (simulation.height / 2)

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
