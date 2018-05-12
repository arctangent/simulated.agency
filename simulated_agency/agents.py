
from .location import Location

class Stateful(object):
    '''
    Represents something which can be created and destroyed,
    and which can also have a state and transition between states.
    '''

    simulation = None
    objects = []

    def __init__(self, state, **state_params):
        # Ensure simulation is set
        assert self.simulation is not None, "Creatable objects must have 'simulation' property set!"
        Stateful.objects.append(self)
        self.set_state(state, **state_params)

    def destroy(self):
        Stateful.objects.remove(self)

    def set_state(self, state_class, **state_params):
        '''
        This function ensures that necessary initialisation
        actions are carried out when an Agent changes state.
        '''
        
        # We pass the kwargs to the state class so it can init correctly
        self.state = state_class(self, **state_params)

    def colour(self):
        return self.state.colour


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
        

class Agent(Cell):
    '''
    Represents a type of agent with a changeable location.
    '''

    def __init__(self, location, state, **state_params):
        super().__init__(location, state, **state_params)

    def move_to_location(self, new_loc):
        '''
        Move the Agent to a directly adjacent location.
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
