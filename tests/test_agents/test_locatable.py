
#
# Test that the loctable object implementation is correct
#

import pytest

from simulated_agency.agents.locatable import Locatable
from simulated_agency.location import Location
from simulated_agency.simulation.simulation import Simulation


#
# Fixtures
#

@pytest.fixture
def simulation():
    return Simulation()

@pytest.fixture
def location(simulation):
    Location.simulation = simulation
    return Location(3, 3)

@pytest.fixture
def Agent(simulation):
    # Returns a class not an instance
    class Agent(Locatable):
        simulation = simulation
    return Agent

#
# Tests
#

def test_new(location, Agent):
    '''
    Check that mass limits in locations are not
    exceeded when objects are created
    '''
    
    agent_one = Agent(location)
    # Ensure that the location is full
    assert location.mass() == location.capacity
    # The real test: ensure we now can't
    # create another agent in the same place
    agent_two = Agent(location)
    assert agent_two is None
    assert Agent.objects == [agent_one]


def test_object_list(location, Agent):

    # Test appended when agent created
    agent = Agent(location)
    assert Agent.objects == [agent]
    # Test removed when agent destroyed
    agent.destroy()
    assert Agent.objects == []
