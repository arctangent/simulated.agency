
from ..states import *
from .types import *
from .stack import *


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
