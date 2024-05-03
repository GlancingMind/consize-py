import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import drop

class TestDropWords(unittest.TestCase):
    def test_drop_success(self):
        stack = ["a"]
        stack = drop(stack)
        expected = []
        self.assertEqual(stack, expected)

    def test_drop_success1(self):
        stack = ["a", "b"]
        stack = drop(stack)
        expected = ["a"]
        self.assertEqual(stack, expected)

    def test_drop_success2(self):
        stack = ["a", "b", "c"]
        stack = drop(stack)
        expected = ["a", "b"]
        self.assertEqual(stack, expected)

    def test_immutability_of_drop(self):
        stack = ["a", "b"]
        drop(stack)
        expected = ["a", "b"]
        self.assertEqual(stack, expected)
