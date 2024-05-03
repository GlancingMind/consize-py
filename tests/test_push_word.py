import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import push

class TestPushWord(unittest.TestCase):
    def test_push_success(self):
        stack = [[], "a"]
        stack = push(stack)
        expected = [["a"]]
        self.assertEqual(stack, expected)

    def test_push_success1(self):
        stack = [["a"], "b"]
        stack = push(stack)
        expected = [["a", "b"]]
        self.assertEqual(stack, expected)

    def test_push_success2(self):
        stack = [["a", "b"], "c"]
        stack = push(stack)
        expected = [["a", "b", "c"]]
        self.assertEqual(stack, expected)

    def test_immutability_of_push(self):
        stack = ["a", [], "b"]
        push(stack)
        expected = ["a", [], "b"]
        self.assertEqual(stack, expected)
