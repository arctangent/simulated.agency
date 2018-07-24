
#
# Test the location module
#

import pytest

from simulated_agency.simulation import Simulation
from simulated_agency.location import Location


#
# Simulation fixtures with different wrapping options
#

@pytest.fixture
def sim_wrap():
    sim_wrap = Simulation(width=10, height=10, cell_size=1)
    return sim_wrap

@pytest.fixture
def sim_no_wrap_x():
    sim_no_wrap_x = Simulation(width=10, height=10, cell_size=1)
    sim_no_wrap_x.wrap_x = False
    return sim_no_wrap_x

@pytest.fixture
def sim_no_wrap_y():
    sim_no_wrap_y = Simulation(width=10, height=10, cell_size=1)
    sim_no_wrap_y.wrap_y = False
    return sim_no_wrap_y

@pytest.fixture
def sim_no_wrap_xy():
    sim_no_wrap_xy = Simulation(width=10, height=10, cell_size=1)
    sim_no_wrap_xy.wrap_x = False
    sim_no_wrap_xy.wrap_y = False
    return sim_no_wrap_xy

#
# Tests
#

# Test Up/Down/Left/Right
# Note that we use `is` comparison because we want to ensure
# they point to the exact same object in memory

def test_up(sim_wrap):
    assert sim_wrap.locations[0, 0].up() is sim_wrap.locations[0, 9]
    assert sim_wrap.locations[5, 5].up() is sim_wrap.locations[5, 4]

def test_up_no_wrap(sim_no_wrap_y):
    assert sim_no_wrap_y.locations[0, 0].up() is sim_no_wrap_y.locations[0, 0]
    assert sim_no_wrap_y.locations[5, 5].up() is sim_no_wrap_y.locations[5, 4]

def test_down(sim_wrap):
    assert sim_wrap.locations[4, 9].down() is sim_wrap.locations[4, 0]
    assert sim_wrap.locations[5, 5].down() is sim_wrap.locations[5, 6]

def test_down_no_wrap(sim_no_wrap_y):
    assert sim_no_wrap_y.locations[4, 9].down() is sim_no_wrap_y.locations[4, 9]
    assert sim_no_wrap_y.locations[5, 5].down() is sim_no_wrap_y.locations[5, 6]

def test_left(sim_wrap):
    assert sim_wrap.locations[0, 7].left() is sim_wrap.locations[9, 7]
    assert sim_wrap.locations[5, 5].left() is sim_wrap.locations[4, 5]

def test_left_no_wrap(sim_no_wrap_x):
    assert sim_no_wrap_x.locations[0, 7].left() is sim_no_wrap_x.locations[0, 7]
    assert sim_no_wrap_x.locations[5, 5].left() is sim_no_wrap_x.locations[4, 5]

def test_right(sim_wrap):
    assert sim_wrap.locations[9, 7].right() is sim_wrap.locations[0, 7]
    assert sim_wrap.locations[5, 5].right() is sim_wrap.locations[6, 5]

def test_right_no_wrap(sim_no_wrap_x):
    assert sim_no_wrap_x.locations[9, 7].right() is sim_no_wrap_x.locations[9, 7]
    assert sim_no_wrap_x.locations[5, 5].right() is sim_no_wrap_x.locations[6, 5]


#
# Test Neighbourhoods
#

# radius == 1

def test_neighbourhood_moore_r1(sim_wrap):
    sim_wrap.neighbourhood_strategy = 'moore'
    l = sim_wrap.locations
    assert l[0, 0].neighbourhood() == { l[9, 9], l[0, 9], l[1, 9], l[9, 0], l[0, 0], l[1, 0], l[9, 1], l[0, 1], l[1, 1] }

def test_neighbourhood_moore_no_wrap_r1(sim_no_wrap_xy):
    sim_no_wrap_xy.neighbourhood_strategy = 'moore'
    l = sim_no_wrap_xy.locations
    assert l[0, 0].neighbourhood() == { l[0, 0], l[1, 0], l[0, 1], l[1, 1] }
    assert l[5, 5].neighbourhood() == { l[4, 4], l[5, 4], l[6, 4], l[4, 5], l[5, 5], l[6, 5], l[4, 6], l[5, 6], l[6, 6] }

def test_neighbourhood_von_neumann_r1(sim_wrap):
    sim_wrap.neighbourhood_strategy = 'von_neumann'
    l = sim_wrap.locations
    assert l[0, 0].neighbourhood() == { l[0, 9], l[9, 0], l[0, 0], l[1, 0], l[0, 1] }

def test_neighbourhood_von_neumann_no_wrap_r1(sim_no_wrap_xy):
    sim_no_wrap_xy.neighbourhood_strategy = 'von_neumann'
    l = sim_no_wrap_xy.locations
    assert l[0, 0].neighbourhood() == { l[0, 0], l[1, 0], l[0, 1] }
    assert l[5, 5].neighbourhood() == { l[5, 5], l[5, 4], l[5, 6], l[4, 5], l[6, 5] }

# radius == 3

def test_neighbourhood_moore_r3(sim_wrap):
    
    sim_wrap.neighbourhood_strategy = 'moore'
    l = sim_wrap.locations
    
    assert l[0, 0].neighbourhood(radius=3) == {
        l[7, 7], l[8, 7], l[9, 7], l[0, 7], l[1, 7], l[2, 7], l[3, 7],
        l[7, 8], l[8, 8], l[9, 8], l[0, 8], l[1, 8], l[2, 8], l[3, 8],
        l[7, 9], l[8, 9], l[9, 9], l[0, 9], l[1, 9], l[2, 9], l[3, 9],
        l[7, 0], l[8, 0], l[9, 0], l[0, 0], l[1, 0], l[2, 0], l[3, 0],
        l[7, 1], l[8, 1], l[9, 1], l[0, 1], l[1, 1], l[2, 1], l[3, 1],
        l[7, 2], l[8, 2], l[9, 2], l[0, 2], l[1, 2], l[2, 2], l[3, 2],
        l[7, 3], l[8, 3], l[9, 3], l[0, 3], l[1, 3], l[2, 3], l[3, 3]
    }


def test_neighbourhood_moore_no_wrap_r3(sim_no_wrap_xy):

    sim_no_wrap_xy.neighbourhood_strategy = 'moore'
    l = sim_no_wrap_xy.locations

    assert l[0, 0].neighbourhood(radius=3) == {
        l[0, 0], l[1, 0], l[2, 0], l[3, 0],
        l[0, 1], l[1, 1], l[2, 1], l[3, 1],
        l[0, 2], l[1, 2], l[2, 2], l[3, 2],
        l[0, 3], l[1, 3], l[2, 3], l[3, 3]
    }
    
    assert l[5, 5].neighbourhood(radius=3) == {
        l[2, 2], l[3, 2], l[4, 2], l[5, 2], l[6, 2], l[7, 2], l[8, 2],
        l[2, 3], l[3, 3], l[4, 3], l[5, 3], l[6, 3], l[7, 3], l[8, 3],
        l[2, 4], l[3, 4], l[4, 4], l[5, 4], l[6, 4], l[7, 4], l[8, 4],
        l[2, 5], l[3, 5], l[4, 5], l[5, 5], l[6, 5], l[7, 5], l[8, 5],
        l[2, 6], l[3, 6], l[4, 6], l[5, 6], l[6, 6], l[7, 6], l[8, 6],
        l[2, 7], l[3, 7], l[4, 7], l[5, 7], l[6, 7], l[7, 7], l[8, 7],
        l[2, 8], l[3, 8], l[4, 8], l[5, 8], l[6, 8], l[7, 8], l[8, 8]
    }


def test_neighbourhood_von_neumann_r3(sim_wrap):

    sim_wrap.neighbourhood_strategy = 'von_neumann'
    l = sim_wrap.locations

    assert l[0, 0].neighbourhood(radius=3) == {
                                   l[0, 7],
                          l[9, 8], l[0, 8], l[1, 8],
                 l[8, 9], l[9, 9], l[0, 9], l[1, 9], l[2, 9],
        l[7, 0], l[8, 0], l[9, 0], l[0, 0], l[1, 0], l[2, 0], l[3, 0],
                 l[8, 1], l[9, 1], l[0, 1], l[1, 1], l[2, 1],
                          l[9, 2], l[0, 2], l[1, 2],
                                   l[0, 3]
    }


def test_neighbourhood_von_neumann_no_wrap_r3(sim_no_wrap_xy):

    sim_no_wrap_xy.neighbourhood_strategy = 'von_neumann'
    l = sim_no_wrap_xy.locations

    assert l[0, 0].neighbourhood(radius=3) == {
        l[0, 0], l[1, 0], l[2, 0], l[3,0],
        l[0, 1], l[1, 1], l[2, 1],
        l[0, 2], l[1, 2],
        l[0, 3]
    }

    assert l[5, 5].neighbourhood(radius=3) == {
                                   l[5, 2],
                          l[4, 3], l[5, 3], l[6, 3],
                 l[3, 4], l[4, 4], l[5, 4], l[6, 4], l[7, 4],
        l[2, 5], l[3, 5], l[4, 5], l[5, 5], l[6, 5], l[7, 5], l[8, 5],
                 l[3, 6], l[4, 6], l[5, 6], l[6, 6], l[7, 6],
                          l[4, 7], l[5, 7], l[6, 7],
                                   l[5, 8] 
    }
