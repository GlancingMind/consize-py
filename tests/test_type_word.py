import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import type

class TestTypeWords(unittest.TestCase):
    def test_type_success(self):
        stack = ["a"]
        type(stack)
        expected = ["wrd"]
        self.assertEqual(stack, expected)

    def test_type_success1(self):
        stack = ["a", "a"]
        type(stack)
        expected = ["a", "wrd"]
        self.assertEqual(stack, expected)

    def test_type_success2(self):
        stack = ["wrd"]
        type(stack)
        expected = ["wrd"]
        self.assertEqual(stack, expected)

    def test_type_success3(self):
        stack = ["[]"]
        type(stack)
        expected = ["wrd"]
        self.assertEqual(stack, expected)

    def test_type_success3(self):
        stack = ["stk"]
        type(stack)
        expected = ["wrd"]
        self.assertEqual(stack, expected)

    def test_type_success4(self):
        stack = ["[", "]"]
        type(stack)
        expected = ["stk"]
        self.assertEqual(stack, expected)

    def test_type_success5(self):
        stack = ["[", "a", "]"]
        type(stack)
        expected = ["stk"]
        self.assertEqual(stack, expected)

    def test_type_success6(self):
        stack = ["10"]
        type(stack)
        expected = ["wrd"]
        self.assertEqual(stack, expected)

