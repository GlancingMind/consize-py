import unittest
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import rot

class TestRotWords(unittest.TestCase):
    def test_rot_success(self):
        stack = ["a", "b", "c"]
        stack = rot(stack)
        expected = ["b", "c", "a"]
        self.assertEqual(stack, expected)

    def test_rot_success1(self):
        stack = ["x", "a", "b", "c"]
        stack = rot(stack)
        expected = ["x", "b", "c", "a"]
        self.assertEqual(stack, expected)

    def test_immutability_of_rot(self):
        stack = ["a", "b", "c"]
        rot(stack)
        expected = ["a", "b", "c"]
        self.assertEqual(stack, expected)
