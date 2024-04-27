import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import emptystack

class TestEmptystackWords(unittest.TestCase):
    def test_emptystack_success(self):
        stack = []
        emptystack(stack)
        expected = [[]]
        self.assertEqual(stack, expected)

    def test_emptystack_success1(self):
        stack = ["0"]
        emptystack(stack)
        expected = ["0", []]
        self.assertEqual(stack, expected)

    def test_emptystack_success2(self):
        stack = ["0", []]
        emptystack(stack)
        expected = ["0", [], []]
        self.assertEqual(stack, expected)
