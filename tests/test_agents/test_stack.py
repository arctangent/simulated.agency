
#
# Test that the stack implementation is correct
#

import unittest

from simulated_agency.agents.stack import Stack


class TestStackMethods(unittest.TestCase):

    def setUp(self):
        # Start all tests with an empty stack
        self.stack = Stack()

    def test_init(self):
        self.assertEqual(self.stack.items, [])

    def test_is_empty(self):
        self.assertTrue(self.stack.is_empty())

    def test_push(self):
        self.stack.push('item_one')
        self.assertEqual(self.stack.items, ['item_one'])
        self.stack.push('item_two')
        self.assertEqual(self.stack.items, ['item_one', 'item_two'])

    def test_pop(self):
        self.stack.items = ['item_one', 'item_two']
        popped = self.stack.pop()
        self.assertEqual(popped, 'item_two')
        self.assertEqual(self.stack.items, ['item_one'])

    def test_peek(self):
        self.stack.items = ['item_one', 'item_two']
        peeked = self.stack.peek()
        self.assertEqual(peeked, 'item_two')
        self.assertEqual(self.stack.items, ['item_one', 'item_two'])

    def test_size(self):
        self.stack.items = ['item_one', 'item_two']
        self.assertEqual(self.stack.size(), 2)

    def test_flush(self):
        self.stack.items = ['item_one', 'item_two']
        self.stack.flush()
        self.assertEqual(self.stack.items, [])


if __name__ == '__main__':
    unittest.main()
