import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import concat

class TestConcatWord(unittest.TestCase):
    def test_concat_emptystacks(self):
        stack = [[], []]
        stack = concat(stack)
        expected = [[]]
        self.assertEqual(stack, expected)

    def test_concat_success1(self):
        stack = [["a"], ["b"]]
        stack = concat(stack)
        expected = [["a", "b"]]
        self.assertEqual(stack, expected)

    def test_concat_success2(self):
        stack = [["a"], ["b"], ["c"]]
        stack = concat(stack)
        expected = [["a"], ["b", "c"]]
        self.assertEqual(stack, expected)

    def test_concat_success3(self):
        stack = [["a"], ["b"], [], ["c"]]
        stack = concat(stack)
        expected = [["a"], ["b"], ["c"]]
        self.assertEqual(stack, expected)

    def test_concat_success4(self):
        stack = [["a"], ["b"], ["c"], []]
        stack = concat(stack)
        expected = [["a"], ["b"], ["c"]]
        self.assertEqual(stack, expected)
