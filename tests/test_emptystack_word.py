import unittest
import sys
import os


# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import InterpreterState

class TestEmptystackWords(unittest.TestCase):
    def test_emptystack_success(self):
        InterpreterState.stack = ["emptystack", "1","2","2","3"]
        InterpreterState.rules.apply(InterpreterState)
        self.assertEqual(["[","]","1","2","2","3"], InterpreterState.stack)

    # def test_emptystack_success1(self):
    #     stack = ["0"]
    #     stack = emptystack(stack)
    #     expected = ["0", []]
    #     self.assertEqual(stack, expected)

    # def test_emptystack_success2(self):
    #     stack = ["0", []]
    #     stack = emptystack(stack)
    #     expected = ["0", [], []]
    #     self.assertEqual(stack, expected)

    # def test_immutability_of_dup(self):
    #     stack = ["a", "b"]
    #     emptystack(stack)
    #     expected = ["a", "b"]
    #     self.assertEqual(stack, expected)
