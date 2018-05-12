

class Createable(object):
    '''
    Represents something which can be created in a world
    and which can also be destroyed (i.e. removed from it)
    '''

    world = None

    def __init__(self, *args, **kwargs):
        # Ensure world is set
        assert self.world is not None, "Locatable objects must have 'world' property set!"
        self.world.agents.append(self)

    def destroy(self):
        self.world.agents.remove(self)


class Locatable(Createable):
    '''
    Represents something which can have a location
    '''

    def __new__(cls, location, *args, **kwargs):
        # We should only create an instance of a thing
        # if the specified location has room for it
        if location.is_full():
            return None

        instance = super().__new__(cls)
        instance.location = location
        return instance

    def __init__(self, location, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = location
        self.location.contents.append(self)
        

    def destroy(self):
        super().destroy()
        self.location.contents.remove(self)
        

class Mobile(Locatable):
    '''
    Represents something which can move around
    '''

    def __init__(self, location, *args, **kwargs):
        super().__init__(location)

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
