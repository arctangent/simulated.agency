
from collections import defaultdict
from random import choice, randint

from .location import Location
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



class Stateful(object):
    '''
    Represents something which can be created and destroyed,
    and which can also have a state and transition between states.
    '''

    simulation = None
    state_machine = None
    objects = []
    # Used for drawing
    size = 1
    # We can use dirty flags to only draw objects when they have changed.
    # We set the flag to True by default so that things are drawn even
    # when the dirty flag functionality is not defined in the State
    dirty = True

    def __init__(self, initial_location, initial_state=None, **kwargs):
        # Ensure simulation is set
        assert self.simulation is not None, "Creatable objects must have 'simulation' property set!"
        # Track agent age
        self.age = 0
        # Init
        Stateful.objects.append(self)
        self._state_stack = Stack()
        # Default state
        self.default_state = MoveRandomly(self)
        # Initial state
        if initial_state:
            self.add_state(initial_state(self, **kwargs))

    def destroy(self):
        Stateful.objects.remove(self)

    def execute(self):
        if self._state_stack.is_empty():
            self._state_stack.push(self.default_state)
        # Delegate to state machine
        self._state_stack.peek().handle()

    def is_in_state(self, state_class):
        return isinstance(self.current_state(), state_class)

    def validate_state(self, state_instance):
        if not isinstance(state_instance, State):
            raise Exception('Not a state instance!')

    def current_state(self):
        ''' Return the top entry of the state stack '''
        return self._state_stack.peek()

    def current_state_class(self):
        ''' Return the class of the top entry of the state stack '''
        return self.current_state().__class__

    def replace_state(self, state_instance):
        ''' Replace the top entry of the state stack with a new state '''
        self.validate_state(state_instance)
        if self._state_stack.size():
            self._state_stack.pop()
        self._state_stack.push(state_instance)

    def add_state(self, state_instance):
        ''' Change state by addind a new state to the state stack '''
        self.validate_state(state_instance)
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


class Cell(Stateful):
    '''
    Represents a type of agent which has an unchangeable location.
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
        return 'Cell with state %s at (%s, %s)' % (self._state_stack.peek(), self.location.x, self.location.y)
        
    def destroy(self):
        # We need to delete the object last
        self.location.contents.remove(self)
        super().destroy()
     

class Agent(Cell):
    '''
    Represents a type of agent with a changeable location.
    '''

    def __init__(self, initial_location, initial_state=None, **kwargs):
        super().__init__(initial_location, initial_state, **kwargs)

    def __repr__(self):
        return 'Agent with state %s at (%s, %s)' % (self._state_stack.peek(), self.location.x, self.location.y)

    def move_to_location(self, new_loc):
        '''
        Move the Agent to a specified adjacent location.
        '''
        
        new_location = Location(new_loc.x, new_loc.y)
        
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
