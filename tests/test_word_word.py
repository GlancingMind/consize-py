import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import word

class TestWordWord(unittest.TestCase):
    def test_word_emptystack(self):
        stack = [[]]
        stack = word(stack)
        expected = [['']]
        self.assertEqual(stack, expected)

    def test_word_success1(self):
        stack = [["a"]]
        stack = word(stack)
        expected = [["a"]]
        self.assertEqual(stack, expected)

    def test_word_success2(self):
        stack = [["a", "b", "c"]]
        stack = word(stack)
        expected = [["abc"]]
        self.assertEqual(stack, expected)

    def test_immutability_of_word(self):
        stack = [["a", "b"]]
        word(stack)
        expected = [["a", "b"]]
        self.assertEqual(stack, expected)
