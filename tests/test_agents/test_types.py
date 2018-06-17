
#
# Test agent metaclass
#

from simulated_agency.agents.types import HasOwnObjectList


def test_hasownobjectlist():
    '''
    The purpose of the metaclass is to ensure that child objects
    maintain their own separate object lists as class variables
    '''

    # Define basic classes which have the metaclass

    class ParentClass(object, metaclass=HasOwnObjectList):
        pass

    class ChildClassOne(ParentClass):
        pass

    class ChildClassTwo(ParentClass):
        pass

    # They should all have empty object lists
    assert ParentClass.objects == []
    assert ChildClassOne.objects == []
    assert ChildClassTwo.objects == []

    # Their object lists should have different memory addresses
    id_pc = id(ParentClass)
    id_cc_one = id(ChildClassOne)
    id_cc_two = id(ChildClassTwo)
    assert id_pc != id_cc_one
    assert id_cc_one != id_cc_two
    assert id_cc_two != id_pc
  