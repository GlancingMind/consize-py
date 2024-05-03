import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import equal

class TestEqualWords(unittest.TestCase):
    def test_equal_success(self):
        stack = ["a", "a"]
        stack = equal(stack)
        expected = ["t"]
        self.assertEqual(stack, expected)

    def test_equal_success1(self):
        stack = ["0", "0"]
        stack = equal(stack)
        expected = ["t"]
        self.assertEqual(stack, expected)

    def test_equal_success2(self):
        stack = ["x", "y", "y"]
        stack = equal(stack)
        expected = ["x", "t"]
        self.assertEqual(stack, expected)

    def test_equal_success3(self):
        stack = ["x", "y"]
        stack = equal(stack)
        expected = ["f"]
        self.assertEqual(stack, expected)

    def test_equal_success2(self):
        stack = ["x", "y", "z"]
        stack = equal(stack)
        expected = ["x", "f"]
        self.assertEqual(stack, expected)

    def test_immutability_of_equal(self):
        stack = ["x", "y"]
        equal(stack)
        expected = ["x", "y"]
        self.assertEqual(stack, expected)
