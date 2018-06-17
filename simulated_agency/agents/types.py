
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
