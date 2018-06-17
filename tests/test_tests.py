
#
# Test whether my tests run
#

import unittest

class TestTests(unittest.TestCase):

    def test_tests(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
