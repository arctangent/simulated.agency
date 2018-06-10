
from random import choice


class Seeder(object):
    '''
    Seeds a simulation with agents
    '''

    def __init__(self, simulation):
        self.simulation = simulation
        # Bind methods
        self.simulation.seed = self.seed
        self.simulation.seed_all = self.seed_all
        self.simulation.create_obstruction_rectangle = self.create_obstruction_rectangle

    def seed(self, object_class, num_or_density, state_class, **kwargs):
        '''
        Create a number of objects within the simulation,
        guaranteed to all be placed (i.e. will retry if
        it randomly chooses a full location.

        Note that since it just retries a new random location
        it isn't well suited to creating dense intial populations
        because the likelihood of choosing an occupied location
        increases as the density rises, leading to more and more
        re-tries being required. However, if you wait long enough
        then it will eventually finish. 

        If num_or_density >= 1 then that is the number
        of objects that will be placed.

        If 0 < num_or_density < 1 then that is the proportion
        of objects that will be placed relative to the area
        of the simulation.

        Returns the number of agents successfully placed.
        '''

        simulation = self.simulation

        # How many objects do we need to place?
        if 0 < num_or_density < 1:
            number_to_place = int(num_or_density * simulation.width * simulation.height)
        elif num_or_density >= 1:
            number_to_place = num_or_density
        else:
            raise Exception("Can't seed %s objects")

        # Begin planting
        for _ in range(0, number_to_place):
            # Find a location
            location_found = False
            while not location_found:
                location = simulation.random_location()
                if location.can_fit(object_class):
                    location_found = True
            # Create the object
            object_class(location, state_class, **kwargs)

        return number_to_place

    def seed_all(self, object_class, possible_state_list):
        '''
        Create an object in every location within the simulation,
        with the initial state chosen at random from possible_states.

        The possible_stats parameter should be a list, with each
        entry being either an unadorned state class name OR a tuple/list.
        If a tuple/list, then the first element should be a state class name
        and then the second element should be a dictionary of state params
        with which to initialise the state.

        Example:
            simulation.seed_all(MyState, [StateOne, [StateTwo, {timer:1}], StateThree]
        '''

        simulation = self.simulation

        for x in range(0, simulation.width):
            for y in range(0, simulation.height):
                location = simulation.locations[x, y]
                object_instance = object_class(location)
                chosen_state = choice(possible_state_list)
                try:
                    # States with params
                    initial_state_class, initial_state_params = chosen_state
                    object_instance.add_state(initial_state_class, **initial_state_params)
                except:
                    # Unadorned states
                    object_instance.add_state(chosen_state)

    def create_obstruction_rectangle(self, x_start, y_start, width, height):
        '''
        Marks a rectangular area of the world as impassable.
        Note: Does not take into account screen wrapping.
        '''

        locations = self.simulation.locations

        for x in range(x_start, x_start + width):
            for y in range(y_start, y_start + height):
                location = locations[x, y]
                location.capacity = 0
                location.colour = "yellow"
