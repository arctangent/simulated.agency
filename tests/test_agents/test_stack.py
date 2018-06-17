
#
# Test that the stack implementation is correct
#

import pytest

from simulated_agency.agents.stack import Stack


@pytest.fixture
def stack():
    ''' Provide an empty stack to each test '''
    return Stack()

def test_init(stack):
    assert stack.items == []

def test_is_empty(stack):
    assert stack.is_empty() is True

def test_push(stack):
    stack.push('item_one')
    assert stack.items == ['item_one']
    stack.push('item_two')
    assert stack.items == ['item_one', 'item_two']

def test_pop(stack):
    stack.items = ['item_one', 'item_two']
    popped = stack.pop()
    assert popped, 'item_two'
    assert stack.items == ['item_one']

def test_peek(stack):
    stack.items = ['item_one', 'item_two']
    peeked = stack.peek()
    assert peeked == 'item_two'
    assert stack.items == ['item_one', 'item_two']

def test_size(stack):
    stack.items = ['item_one', 'item_two']
    assert stack.size() == 2

def test_flush(stack):
    stack.items = ['item_one', 'item_two']
    stack.flush()
    assert stack.items == []
