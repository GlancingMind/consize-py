import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import unmap, mapping

class TestUnmapWord(unittest.TestCase):
    def test_unmap_empty_dict(self):
        stack = [{}]
        stack = unmap(stack)
        expected = [[]]
        self.assertEqual(stack, expected)

    def test_unmap_success1(self):
        stack = [{"a": 1}]
        stack = unmap(stack)
        expected = [["a", 1]]
        self.assertEqual(stack, expected)

    def test_unmap_success2(self):
        stack = [{"a": 1, "b": 2}]
        stack = unmap(stack)
        expected = [["a", 1, "b", 2]]
        self.assertEqual(stack, expected)

    def test_unmap_success3(self):
        stack = [["a", 1, "b", 2]]
        stack = unmap(mapping(stack))
        expected = [["a", 1, "b", 2]]
        self.assertEqual(stack, expected)

    def test_unmap_success4(self):
        stack = ["b", {"a": 1}]
        stack = unmap(stack)
        expected = ["b", ["a", 1]]
        self.assertEqual(stack, expected)
