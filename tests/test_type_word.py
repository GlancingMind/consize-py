import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import type

class TestTypeWords(unittest.TestCase):
    def test_type_success(self):
        stack = ["a"]
        stack = type(stack)
        expected = ["wrd"]
        self.assertEqual(stack, expected)

    def test_type_success1(self):
        stack = ["a", "a"]
        stack = type(stack)
        expected = ["a", "wrd"]
        self.assertEqual(stack, expected)

    def test_type_success2(self):
        stack = ["wrd"]
        stack = type(stack)
        expected = ["wrd"]
        self.assertEqual(stack, expected)

    def test_type_success3(self):
        stack = ["[]"]
        stack = type(stack)
        expected = ["wrd"]
        self.assertEqual(stack, expected)

    def test_type_success3(self):
        stack = ["stk"]
        stack = type(stack)
        expected = ["wrd"]
        self.assertEqual(stack, expected)

    def test_type_success4(self):
        stack = [[]]
        stack = type(stack)
        expected = ["stk"]
        self.assertEqual(stack, expected)

    def test_type_success5(self):
        stack = [["a"]]
        stack = type(stack)
        expected = ["stk"]
        self.assertEqual(stack, expected)

    def test_type_success6(self):
        stack = ["10"]
        stack = type(stack)
        expected = ["wrd"]
        self.assertEqual(stack, expected)

    def test_type_success7(self):
        stack = [{}]
        stack = type(stack)
        expected = ["map"]
        self.assertEqual(stack, expected)

    def test_type_success8(self):
        stack = [{"a": 1}]
        stack = type(stack)
        expected = ["map"]
        self.assertEqual(stack, expected)

    def test_type_success9(self):
        stack = [(lambda: "Hello World!")]
        stack = type(stack)
        expected = ["fct"]
        self.assertEqual(stack, expected)

    def test_type_success10(self):
        stack = [None]
        stack = type(stack)
        expected = ["nil"]
        self.assertEqual(stack, expected)

    def test_type_replace_only_top_element(self):
        stack = ["x", {"a": 1}]
        stack = type(stack)
        expected = ["x", "map"]
        self.assertEqual(stack, expected)

    def test_immutability_of_type(self):
        stack = ["a", "b"]
        type(stack)
        expected = ["a", "b"]
        self.assertEqual(stack, expected)
