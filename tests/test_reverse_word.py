import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import reverse

class TestReverseWord(unittest.TestCase):
    def test_reverse_emptystack(self):
        stack = []
        stack = reverse(stack)
        expected = []
        self.assertEqual(stack, expected)

    def test_pop_success1(self):
        stack = ["a"]
        stack = reverse(stack)
        expected = ["a"]
        self.assertEqual(stack, expected)

    def test_pop_success2(self):
        stack = ["a", "b", "c"]
        stack = reverse(stack)
        expected = ["c", "b", "a"]
        self.assertEqual(stack, expected)

    def test_immutability_of_reverse(self):
        stack = [["a", "b"]]
        reverse(stack)
        expected = [["a", "b"]]
        self.assertEqual(stack, expected)
