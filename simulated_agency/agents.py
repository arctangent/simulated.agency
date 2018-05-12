
from collections import defaultdict
from random import choice, randint

from .location import Location
from .states import StateMachine

class Stateful(object):
    '''
    Represents something which can be created and destroyed,
    and which can also have a state and transition between states.
    '''

    simulation = None
    state_machine = None
    objects = []

    def __init__(self, state, **state_params):
        # Ensure simulation is set
        assert self.simulation is not None, "Creatable objects must have 'simulation' property set!"
        # Ensure state machine is set
        assert self.state_machine is not None, "Creatable objects must have 'state_machine' property set!"
        # Init
        self.memory = defaultdict(None)
        Stateful.objects.append(self)
        self.set_state(state, **state_params)

    def destroy(self):
        Stateful.objects.remove(self)
        del(self)

    def set_state(self, state_class, **state_params):
        '''
        This function ensures that necessary initialisation
        actions are carried out when an Agent changes state.
        '''
        
        # Check all required params are there
        if hasattr(state_class, 'required_params'):
            if not all(key in state_params for key in state_class.required_params):
                raise Exception('Not all required params passed to %s' % state_class)
        self.state_name = state_class.name
        self.memory.update(**state_params)

    def execute(self):
        # Delegate to state machine
        self.state_machine.execute(self)

    def colour(self):
        return self.state_machine.get_state_by_name(self.state_name).colour


class Cell(Stateful):
    '''
    Represents a type of agent which has an unchangeable location.
    '''

    def __new__(cls, location, *args, **kwargs):
        # We should only create an instance of a thing
        # if the specified location has room for it
        if location.is_full():
            return None

        instance = super().__new__(cls)
        return instance

    def __init__(self, location, state, **state_params):
        super().__init__(state, **state_params)      
        self.location = location
        self.location.contents.append(self)  

    def destroy(self):
        super().destroy()
        self.location.contents.remove(self)

    def __repr__(self):
        return 'Cell with state %s at (%s, %s)' % (self.state_name, self.location.x, self.location.y)
        

class Agent(Cell):
    '''
    Represents a type of agent with a changeable location.
    '''

    def __init__(self, location, state, **state_params):
        super().__init__(location, state, **state_params)

    def __repr__(self):
        return 'Cell with state %s at (%s, %s)' % (self.state_name, self.location.x, self.location.y)

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
