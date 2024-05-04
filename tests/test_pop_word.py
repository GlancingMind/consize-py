import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import pop

class TestPopWord(unittest.TestCase):
    def test_pop_emptystack(self):
        stack = []
        stack = pop(stack)
        expected = []
        self.assertEqual(stack, expected)

    def test_pop_success1(self):
        stack = ["a"]
        stack = pop(stack)
        expected = []
        self.assertEqual(stack, expected)

    def test_pop_success2(self):
        stack = ["a", "b", "c"]
        stack = pop(stack)
        expected = ["b", "c"]
        self.assertEqual(stack, expected)

    def test_immutability_of_pop(self):
        stack = ["a", "b"]
        pop(stack)
        expected = ["a", "b"]
        self.assertEqual(stack, expected)
