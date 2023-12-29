import unittest

from sample import add


class TestSample(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(-1, 2), 1)
        self.assertEqual(add(0, 0), 0)
        self.assertEqual(add(-1, -1), -2)

if __name__ == '__main__':
    unittest.main()
