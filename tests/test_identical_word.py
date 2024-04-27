import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import identical

class TestIdenticalWords(unittest.TestCase):
    def test_equal_success(self):
        stack = ["a", "a"]
        identical(stack)
        expected = ["t"]
        self.assertEqual(stack, expected)

    def test_equal_success1(self):
        stack = ["0", "0"]
        identical(stack)
        expected = ["t"]
        self.assertEqual(stack, expected)

    def test_equal_success2(self):
        stack = ["x", "y", "y"]
        identical(stack)
        expected = ["x", "t"]
        self.assertEqual(stack, expected)

    def test_equal_success3(self):
        stack = ["x", "y"]
        identical(stack)
        expected = ["f"]
        self.assertEqual(stack, expected)

    def test_equal_success2(self):
        stack = ["x", "y", "z"]
        identical(stack)
        expected = ["x", "f"]
        self.assertEqual(stack, expected)
