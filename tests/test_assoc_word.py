import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import assoc

class TestAssocWord(unittest.TestCase):
    def test_assoc_success(self):
        stack = ["a", 1, {}]
        stack = assoc(stack)
        expected = [{"a": 1}]
        self.assertEqual(stack, expected)

    def test_assoc_success1(self):
        stack = ["a", 1, {"b": 2}]
        stack = assoc(stack)
        expected = [{"a": 1, "b": 2}]
        self.assertEqual(stack, expected)

    def test_assoc_success2(self):
        stack = ["x", "a", 1, {"b": 2}]
        stack = assoc(stack)
        expected = ["x", {"a": 1, "b": 2}]
        self.assertEqual(stack, expected)

    def test_immutability_of_assoc(self):
        stack = ["x", "a", 1, {"b": 2}]
        assoc(stack)
        expected = ["x", "a", 1, {"b": 2}]
        self.assertEqual(stack, expected)
