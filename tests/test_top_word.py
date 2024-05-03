import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import top

class TestTopWord(unittest.TestCase):
    def test_top_success(self):
        stack = [["a"]]
        stack = top(stack)
        expected = ["a"]
        self.assertEqual(stack, expected)

    def test_top_success1(self):
        stack = [["a", "b"]]
        stack = top(stack)
        expected = ["a"]
        self.assertEqual(stack, expected)

    def test_top_success2(self):
        stack = [[]]
        stack = top(stack)
        expected = ["nil"]
        self.assertEqual(stack, expected)

    def test_top_success3(self):
        stack = [None]
        stack = top(stack)
        expected = ["nil"]
        self.assertEqual(stack, expected)

    def test_immutability_of_top(self):
        stack = ["a", "b"]
        top(stack)
        expected = ["a", "b"]
        self.assertEqual(stack, expected)
