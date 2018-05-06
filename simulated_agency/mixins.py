



class Locatable(object):
    '''
    Represents something which can have a location
    '''

    def __init__(self, location=None, *args, **kwargs):
        self.location = location


class Mobile(Locatable):
    '''
    Represents something which can move around
    '''

    def __init__(self, location=None, *args, **kwargs):
        super().__init__(location, *args, **kwargs)

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
