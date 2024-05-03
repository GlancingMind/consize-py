import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import keys

class TestKeysWord(unittest.TestCase):
    def test_keys_empty_dict(self):
        stack = [{}]
        stack = keys(stack)
        expected = [[]]
        self.assertEqual(stack, expected)

    def test_keys_success(self):
        stack = [{"a": 1}]
        stack = keys(stack)
        expected = [["a"]]
        self.assertEqual(stack, expected)

    def test_keys_success1(self):
        stack = [{"a": 1, "b": 2}]
        stack = keys(stack)
        expected = [["a", "b"]]
        self.assertEqual(stack, expected)

    def test_keys_success2(self):
        stack = ["x", {"a": 1, "b": 2}]
        stack = keys(stack)
        expected = ["x", ["a", "b"]]
        self.assertEqual(stack, expected)
