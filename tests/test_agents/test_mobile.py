
#
# Test that the mobile object implementation is correct
#

import pytest

from simulated_agency.agents.mobile import Mobile
from simulated_agency.simulation.simulation import Simulation


#
# Fixtures
#

@pytest.fixture
def simulation():
    return Simulation()

@pytest.fixture
def locations(simulation):
    return simulation.locations

@pytest.fixture
def Agent(simulation):
    class Agent(Mobile):
        simulation = simulation
    return Agent


#
# Tests
#

def test_relocate(Agent, locations):
    # Ensure the location is correct to start with
    agent = Agent(locations[3, 3])
    assert agent.location == locations[3, 3]
    assert locations[3, 3].contents == [agent]
    # Perform relocation and check again
    agent._relocate(locations[5, 7])
    assert agent.location == locations[5, 7]
    assert locations[3, 3].contents == []
    assert locations[5, 7].contents == [agent]


def test_move_to_location(Agent, locations):
    
    # Simple case: target location can fit agent
    agent = Agent(locations[3, 3])
    agent.move_to_location(locations[5, 7])
    assert agent.location == locations[5, 7]
    
    # More complex case: target location cannot fit agent
    # Branch A: Alternative(s) specified
    # Branch B: No alternatives specified

    #
    # Branch A
    #

    agent_one = Agent(locations[6, 2])
    agent_two = Agent(locations[7, 4])
    # Ensure we definitely can't move agent_one
    # to same location as agent_two
    assert agent_two.location.can_fit(agent_one) is False
    # Attempt the move anyway, but provide some alternatives
    alternatives = [
        locations[9, 1],
        locations[8, 3]
    ]
    agent_one.move_to_location(agent_two.location, alt_moves=alternatives)
    assert agent_one.location in alternatives

    #
    # Branch B
    #

    agent_three = Agent(locations[1, 1])
    agent_four = Agent(locations[3, 8])
    # Ensure we definitely can't move agent_three
    # to same location as agent_four
    assert agent_four.location.can_fit(agent_three) is False
    # Attempt the move anyway, without providing any alternatives
    agent_three.move_to_location(agent_four.location)
    # Ensure we didn't move to the illegal location
    assert agent_three.location != agent_four.location
