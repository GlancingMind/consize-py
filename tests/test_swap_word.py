import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import swap

class TestSwapWords(unittest.TestCase):
    def test_swap_success(self):
        stack = ["a", "b"]
        stack = swap(stack)
        expected = ["b", "a"]
        self.assertEqual(stack, expected)

    def test_swap_success1(self):
        stack = ["a", "b", "c"]
        stack = swap(stack)
        expected = ["a", "c", "b"]
        self.assertEqual(stack, expected)

    def test_immutability_of_swap(self):
        stack = ["a", "b"]
        swap(stack)
        expected = ["a", "b"]
        self.assertEqual(stack, expected)
