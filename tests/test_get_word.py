import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import get

class TestGetWord(unittest.TestCase):
    def test_get_from_empty_dict(self):
        stack = ["a", {}, 'z']
        stack = get(stack)
        expected = ['z']
        self.assertEqual(stack, expected)

    def test_get_success(self):
        stack = ["b", {"b": 2}, 'z']
        stack = get(stack)
        expected = [2]
        self.assertEqual(stack, expected)

    def test_get_success1(self):
        stack = ["a", {"a": 1, "b": 2}, 'z']
        stack = get(stack)
        expected = [1]
        self.assertEqual(stack, expected)

    def test_get_success2(self):
        stack = ["x", "a", {"a": 1, "b": 2}, 'z']
        stack = get(stack)
        expected = ["x", 1]
        self.assertEqual(stack, expected)

    def test_immutability_of_get(self):
        stack = ["x", "a", 1, {"b": 2}, 'z']
        get(stack)
        expected = ["x", "a", 1, {"b": 2}, 'z']
        self.assertEqual(stack, expected)
