import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import dissoc

class TestDissocWord(unittest.TestCase):
    def test_dissoc_removale_from_empty_dict(self):
        stack = ["a", {}]
        stack = dissoc(stack)
        expected = [{}]
        self.assertEqual(stack, expected)

    def test_dissoc_removal_of_non_existing_entry(self):
        stack = ["a", {"b": 2}]
        stack = dissoc(stack)
        expected = [{"b": 2}]
        self.assertEqual(stack, expected)

    def test_dissoc_success(self):
        stack = ["b", {"b": 2}]
        stack = dissoc(stack)
        expected = [{}]
        self.assertEqual(stack, expected)

    def test_dissoc_success1(self):
        stack = ["a", {"a": 1, "b": 2}]
        stack = dissoc(stack)
        expected = [{"b": 2}]
        self.assertEqual(stack, expected)

    def test_dissoc_success2(self):
        stack = ["x", "a", {"a": 1, "b": 2}]
        stack = dissoc(stack)
        expected = ["x", {"b": 2}]
        self.assertEqual(stack, expected)

    def test_immutability_of_dissoc(self):
        stack = ["x", "a", 1, {"b": 2}]
        dissoc(stack)
        expected = ["x", "a", 1, {"b": 2}]
        self.assertEqual(stack, expected)
