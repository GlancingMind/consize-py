import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import merge

class TestMergeWord(unittest.TestCase):
    def test_merge_of_empty_dicts(self):
        stack = [{}, {}]
        stack = merge(stack)
        expected = [{}]
        self.assertEqual(stack, expected)

    def test_merge_success(self):
        stack = [{"a": 1}, {"b": 2}]
        stack = merge(stack)
        expected = [{"a": 1, "b": 2}]
        self.assertEqual(stack, expected)

    def test_merge_success1(self):
        stack = [{"a": 1, "c": 3}, {"b": 2}]
        stack = merge(stack)
        expected = [{"a": 1, "b": 2, "c": 3}]
        self.assertEqual(stack, expected)

    def test_merge_success2(self):
        stack = [{"a": 1}, {"b": 2, "c": 3}]
        stack = merge(stack)
        expected = [{"a": 1, "b": 2, "c": 3}]
        self.assertEqual(stack, expected)

    def test_merge_success3(self):
        stack = [{"a": 1}, {"a": 2, "c": 3}]
        stack = merge(stack)
        expected = [{"a": 2, "c": 3}]
        self.assertEqual(stack, expected)

    def test_merge_success4(self):
        stack = [{"a": 1}, {"a": 2, "c": 3}]
        stack = merge(stack)
        expected = [{"a": 2, "c": 3}]
        self.assertEqual(stack, expected)

    def test_merge_success5(self):
        stack = [{"a": 1, "c": 3}, {"a": 5, "b": 2}]
        stack = merge(stack)
        expected = [{"a": 5, "b": 2, "c": 3}]
        self.assertEqual(stack, expected)

    def test_merge_success3(self):
        stack = ["x", {"a": 1}, {"b": 2, "c": 3}]
        stack = merge(stack)
        expected = ["x", {"a": 1, "b": 2, "c": 3}]
        self.assertEqual(stack, expected)

    def test_immutability_of_merge(self):
        stack = [{"a": 1}, {"b": 2}]
        merge(stack)
        expected = [{"a": 1}, {"b": 2}]
        self.assertEqual(stack, expected)
