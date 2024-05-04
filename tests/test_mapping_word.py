import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import mapping

class TestMappingWord(unittest.TestCase):
    def test_mapping_emptystack(self):
        stack = [[]]
        stack = mapping(stack)
        expected = [{}]
        self.assertEqual(stack, expected)

    def test_mapping_success1(self):
        stack = [["a", 1]]
        stack = mapping(stack)
        expected = [{"a": 1}]
        self.assertEqual(stack, expected)

    def test_mapping_success2(self):
        stack = ["z", ["a", 1]]
        stack = mapping(stack)
        expected = ["z", {"a": 1}]
        self.assertEqual(stack, expected)

    def test_mapping_success3(self):
        stack = ["z", ["a", 1, "b", 2]]
        stack = mapping(stack)
        expected = ["z", {"a": 1, "b": 2}]
        self.assertEqual(stack, expected)

    def test_immutability_of_mapping(self):
        stack = ["z", ["a", 1, "b", 2]]
        mapping(stack)
        expected = ["z", ["a", 1, "b", 2]]
        self.assertEqual(stack, expected)
