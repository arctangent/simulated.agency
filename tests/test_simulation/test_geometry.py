
#
# Test that the geometry module works correctly
#


import pytest

from simulated_agency.simulation.simulation import Simulation
from simulated_agency.simulation.geometry import Geometry
from simulated_agency.location import Location


#
# Tests - private methods
#

def test_wrap():
    ''' Test the internal _wrap method of geometry class
    '''

    s = Simulation(width=10, height=10, cell_size=1)
    g = Geometry(s)
    
    # Test value less than minimum
    assert g._wrap(-1, 0, 9) == 9
    # Test value more than maximum
    assert g._wrap(10, 0, 9) == 0
    # Test value in acceptable range
    assert g._wrap(5, 0, 9) == 5

def test_constrain():
    ''' Test the internal _constrain method of geometry class
    '''

    s = Simulation(width=10, height=10, cell_size=1)
    g = Geometry(s)

    # Test value less than minimum
    assert g._constrain(-1, 0, 9) == 0
    # Test value more than maximum
    assert g._constrain(10, 0, 9) == 9
    # Test value in acceptable range
    assert g._constrain(5, 0, 9) == 5

#
# Tests - normalisation
#

def test_normalise_width():

    s = Simulation(width=10, height=10, cell_size=1)

    # Test with wrapping
    s.wrap_x = True
    assert s.normalise_width(-1) == 9
    assert s.normalise_width(10) == 0
    assert s.normalise_width(5) == 5

    # Test without wrapping
    s.wrap_x = False
    assert s.normalise_width(-1) == 0
    assert s.normalise_width(10) == 9
    assert s.normalise_width(5) == 5


def test_normalise_height():

    s = Simulation(width=10, height=10, cell_size=1)

    # Test with wrapping
    s.wrap_y = True
    assert s.normalise_height(-1) == 9
    assert s.normalise_height(10) == 0
    assert s.normalise_height(5) == 5

    # Test without wrapping
    s.wrap_y = False
    assert s.normalise_height(-1) == 0
    assert s.normalise_height(10) == 9
    assert s.normalise_height(5) == 5


#
# Tests - random coordinates
#

def test_random_x():
    s = Simulation(width=10, height=10, cell_size=1)
    assert 0 <= s.random_x() <= s.width - 1

def test_random_y():
    s = Simulation(width=10, height=10, cell_size=1)
    assert 0 <= s.random_y() <= s.height - 1

def test_random_xy():
    s = Simulation(width=10, height=10, cell_size=1)
    x, y = s.random_xy()
    assert 0 <= x <= s.width - 1
    assert 0 <= y <= s.height - 1

def test_random_location():
    s = Simulation(width=10, height=10, cell_size=1)
    assert isinstance(s.random_location(), Location)


#
# Tests - distances etc.
#

def test_vector_between():

    s = Simulation(width=10, height=10, cell_size=1)
    l = s.locations
    loc_00 = l[0, 0]
    loc_01 = l[0, 1]
    loc_11 = l[1, 1]
    loc_99 = l[9, 9]

    # Test with wrapping
    s.wrap_x = True
    s.wrap_y = True
    assert s.vector_between(loc_00.x, loc_00.y, loc_01.x, loc_01.y) == (0, 1)
    assert s.vector_between(loc_00.x, loc_00.y, loc_11.x, loc_11.y) == (1, 1)
    assert s.vector_between(loc_00.x, loc_00.y, loc_99.x, loc_99.y) == (-1, -1)

    # Test without wrapping
    s.wrap_x = False
    s.wrap_y = False
    assert s.vector_between(loc_00.x, loc_00.y, loc_01.x, loc_01.y) == (0, 1)
    assert s.vector_between(loc_00.x, loc_00.y, loc_11.x, loc_11.y) == (1, 1)
    assert s.vector_between(loc_00.x, loc_00.y, loc_99.x, loc_99.y) == (9, 9)


def test_distance_between():

    s = Simulation(width=10, height=10, cell_size=1)
    l = s.locations
    loc_00 = l[0, 0]
    loc_01 = l[0, 1]
    loc_11 = l[1, 1]
    loc_99 = l[9, 9]

    # Test with wrapping
    s.wrap_x = True
    s.wrap_y = True
    assert s.distance_between(loc_00, loc_01) == 1
    assert s.distance_between(loc_00, loc_11) == 2 ** 0.5
    assert s.distance_between(loc_00, loc_99) == 2 ** 0.5

    # Test without wrapping
    s.wrap_x = False
    s.wrap_y = False
    assert s.distance_between(loc_00, loc_01) == 1
    assert s.distance_between(loc_00, loc_11) == 2 ** 0.5
    assert s.distance_between(loc_00, loc_99) == 162 ** 0.5


def test_nearest():

    s = Simulation(width=10, height=10, cell_size=1)
    l = s.locations
    loc_00 = l[0, 0]
    loc_01 = l[0, 1]
    loc_10 = l[1, 0]
    loc_11 = l[1, 1]
    loc_33 = l[3, 3]
    loc_99 = l[9, 9]

    # Test with wrapping
    s.wrap_x = True
    s.wrap_y = True
    assert s.nearest(loc_00, [loc_11, loc_33]) == loc_11
    assert s.nearest(loc_00, [loc_01, loc_10]) in [loc_01, loc_10]
    assert s.nearest(loc_00, [loc_33, loc_99]) == loc_99

    # Test without wrapping
    s.wrap_x = False
    s.wrap_y = False
    assert s.nearest(loc_00, [loc_11, loc_33]) == loc_11
    assert s.nearest(loc_00, [loc_01, loc_10]) in [loc_01, loc_10]
    assert s.nearest(loc_00, [loc_33, loc_99]) == loc_33
