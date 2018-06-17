
#
# Test that the stateful object implementation is correct
#

import pytest

from simulated_agency.agents.stateful import Stateful
from simulated_agency.simulation.simulation import Simulation
from simulated_agency.states import State


#
# Tests
#

def test_simulation_requirement():
    '''
    We should not be able to instantiate a Stateful
    object without specifying the simulation
    '''

    class Agent(Stateful):
        pass

    # Without simulation unspecified
    with pytest.raises(Exception):
        dummy = Agent()

    # With simulation specified
    Agent.simulation = Simulation()
    dummy = Agent()


def test_object_list():

    class Agent(Stateful):
        simulation = Simulation()

    # Test appended when agent created
    agent = Agent()
    assert Agent.objects == [agent]
    # Test removed when agent destroyed
    agent.destroy()
    assert Agent.objects == []


def test_state_management():

    class StateOne(State):
        def handle(self):
            super().handle()

    class StateTwo(State):
        def handle(self):
            super().handle()

    class Agent(Stateful):
        simulation = Simulation()

    # Initial state, and testing for state
    agent = Agent(initial_state=StateOne)
    assert agent.is_in_state(StateOne)

    # Replacing state
    agent.replace_state(StateTwo)
    assert agent.is_in_state(StateTwo)

    # Add and remove states
    agent.add_state(StateOne)
    assert agent.is_in_state(StateOne)
    agent.remove_state()
    assert agent.is_in_state(StateTwo)



