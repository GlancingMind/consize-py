import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import identical

class TestIdenticalWords(unittest.TestCase):
    def test_identical_success(self):
        stack = ["a", "a"]
        stack = identical(stack)
        expected = ["t"]
        self.assertEqual(stack, expected)

    def test_identical_success1(self):
        stack = ["0", "0"]
        stack = identical(stack)
        expected = ["t"]
        self.assertEqual(stack, expected)

    def test_identical_success2(self):
        stack = ["x", "y", "y"]
        stack = identical(stack)
        expected = ["x", "t"]
        self.assertEqual(stack, expected)

    def test_identical_success3(self):
        stack = ["x", "y"]
        stack = identical(stack)
        expected = ["f"]
        self.assertEqual(stack, expected)

    def test_identical_success2(self):
        stack = ["x", "y", "z"]
        stack = identical(stack)
        expected = ["x", "f"]
        self.assertEqual(stack, expected)

    def test_immutability_of_identical(self):
        stack = ["x", "y"]
        identical(stack)
        expected = ["x", "y"]
        self.assertEqual(stack, expected)
