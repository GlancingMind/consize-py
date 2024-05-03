import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import dup

class TestDupWords(unittest.TestCase):
    def test_dup_success(self):
        stack = ["a"]
        stack = dup(stack)
        expected = ["a", "a"]
        self.assertEqual(stack, expected)

    def test_dup_success1(self):
        stack = ["a", "b"]
        stack = dup(stack)
        expected = ["a", "b", "b"]
        self.assertEqual(stack, expected)

    def test_immutability_of_dup(self):
        stack = ["a", "b"]
        dup(stack)
        expected = ["a", "b"]
        self.assertEqual(stack, expected)
