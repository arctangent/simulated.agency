
#
# Test that the geometry module works correctly
#


import pytest

from simulated_agency.simulation.simulation import Simulation
from simulated_agency.simulation.geometry import Geometry
from simulated_agency.location import Location



#
# Simulation fixtures with different wrapping options
#

@pytest.fixture
def sim_wrap():
    sim_wrap = Simulation(width=10, height=10, cell_size=1)
    return sim_wrap

@pytest.fixture
def sim_no_wrap_xy():
    sim_no_wrap_xy = Simulation(width=10, height=10, cell_size=1)
    sim_no_wrap_xy.wrap_x = False
    sim_no_wrap_xy.wrap_y = False
    return sim_no_wrap_xy


#
# Tests - private methods
#

def test_wrap(sim_wrap):
    ''' Test the internal _wrap method of geometry class
    '''

    g = Geometry(sim_wrap)
    
    # Test value less than minimum
    assert g._wrap(-1, 0, 9) == 9
    # Test value more than maximum
    assert g._wrap(10, 0, 9) == 0
    # Test value in acceptable range
    assert g._wrap(5, 0, 9) == 5

def test_constrain(sim_wrap):
    ''' Test the internal _constrain method of geometry class
    '''

    g = Geometry(sim_wrap)

    # Test value less than minimum
    assert g._constrain(-1, 0, 9) == 0
    # Test value more than maximum
    assert g._constrain(10, 0, 9) == 9
    # Test value in acceptable range
    assert g._constrain(5, 0, 9) == 5

#
# Tests - normalisation
#

def test_normalise_width_with_wrap(sim_wrap):

    assert sim_wrap.normalise_width(-1) == 9
    assert sim_wrap.normalise_width(10) == 0
    assert sim_wrap.normalise_width(5) == 5


def test_normalise_width_without_wrap(sim_no_wrap_xy):

    assert sim_no_wrap_xy.normalise_width(-1) == 0
    assert sim_no_wrap_xy.normalise_width(10) == 9
    assert sim_no_wrap_xy.normalise_width(5) == 5


def test_normalise_height_with_wrap(sim_wrap):

    assert sim_wrap.normalise_height(-1) == 9
    assert sim_wrap.normalise_height(10) == 0
    assert sim_wrap.normalise_height(5) == 5


def test_normalise_height_without_wrap(sim_no_wrap_xy):

    assert sim_no_wrap_xy.normalise_height(-1) == 0
    assert sim_no_wrap_xy.normalise_height(10) == 9
    assert sim_no_wrap_xy.normalise_height(5) == 5


#
# Tests - random coordinates
#

def test_random_x(sim_wrap):
    assert 0 <= sim_wrap.random_x() <= sim_wrap.width - 1

def test_random_y(sim_wrap):
    assert 0 <= sim_wrap.random_y() <= sim_wrap.height - 1

def test_random_xy(sim_wrap):
    x, y = sim_wrap.random_xy()
    assert 0 <= x <= sim_wrap.width - 1
    assert 0 <= y <= sim_wrap.height - 1

def test_random_location(sim_wrap):
    assert isinstance(sim_wrap.random_location(), Location)


#
# Tests - distances etc.
#

def test_vector_between_with_wrap(sim_wrap):

    l = sim_wrap.locations
    loc_00 = l[0, 0]
    loc_01 = l[0, 1]
    loc_11 = l[1, 1]
    loc_99 = l[9, 9]

    assert sim_wrap.vector_between(loc_00.x, loc_00.y, loc_01.x, loc_01.y) == (0, 1)
    assert sim_wrap.vector_between(loc_00.x, loc_00.y, loc_11.x, loc_11.y) == (1, 1)
    assert sim_wrap.vector_between(loc_00.x, loc_00.y, loc_99.x, loc_99.y) == (-1, -1)

def test_vector_between_without_wrap(sim_no_wrap_xy):

    l = sim_no_wrap_xy.locations
    loc_00 = l[0, 0]
    loc_01 = l[0, 1]
    loc_11 = l[1, 1]
    loc_99 = l[9, 9]

    assert sim_no_wrap_xy.vector_between(loc_00.x, loc_00.y, loc_01.x, loc_01.y) == (0, 1)
    assert sim_no_wrap_xy.vector_between(loc_00.x, loc_00.y, loc_11.x, loc_11.y) == (1, 1)
    assert sim_no_wrap_xy.vector_between(loc_00.x, loc_00.y, loc_99.x, loc_99.y) == (9, 9)


def test_distance_between_with_wrap(sim_wrap):
    ''' Note that we use Manhattan distances
    '''

    l = sim_wrap.locations
    loc_00 = l[0, 0]
    loc_01 = l[0, 1]
    loc_11 = l[1, 1]
    loc_99 = l[9, 9]

    assert sim_wrap.distance_between(loc_00, loc_01) == 1
    assert sim_wrap.distance_between(loc_00, loc_11) == 2
    assert sim_wrap.distance_between(loc_00, loc_99) == 2

def test_distance_between_without_wrap(sim_no_wrap_xy):
    ''' Note that we use Manhattan distances
    '''

    l = sim_no_wrap_xy.locations
    loc_00 = l[0, 0]
    loc_01 = l[0, 1]
    loc_11 = l[1, 1]
    loc_99 = l[9, 9]

    assert sim_no_wrap_xy.distance_between(loc_00, loc_01) == 1
    assert sim_no_wrap_xy.distance_between(loc_00, loc_11) == 2
    assert sim_no_wrap_xy.distance_between(loc_00, loc_99) == 18


def test_nearest_with_wrap(sim_wrap):

    l = sim_wrap.locations
    loc_00 = l[0, 0]
    loc_01 = l[0, 1]
    loc_10 = l[1, 0]
    loc_11 = l[1, 1]
    loc_33 = l[3, 3]
    loc_99 = l[9, 9]

    assert sim_wrap.nearest(loc_00, [loc_11, loc_33]) == loc_11
    assert sim_wrap.nearest(loc_00, [loc_01, loc_10]) in [loc_01, loc_10]
    assert sim_wrap.nearest(loc_00, [loc_33, loc_99]) == loc_99


def test_nearest_without_wrap(sim_no_wrap_xy):

    l = sim_no_wrap_xy.locations
    loc_00 = l[0, 0]
    loc_01 = l[0, 1]
    loc_10 = l[1, 0]
    loc_11 = l[1, 1]
    loc_33 = l[3, 3]
    loc_99 = l[9, 9]

    assert sim_no_wrap_xy.nearest(loc_00, [loc_11, loc_33]) == loc_11
    assert sim_no_wrap_xy.nearest(loc_00, [loc_01, loc_10]) in [loc_01, loc_10]
    assert sim_no_wrap_xy.nearest(loc_00, [loc_33, loc_99]) == loc_33
