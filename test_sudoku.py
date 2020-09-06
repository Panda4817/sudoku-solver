import unittest
import io
import termcolor
from unittest.mock import patch
import numpy
from sudoku import *


class SudokuTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Test boards
        cls.four = numpy.zeros((4, 4), dtype=int)
        cls.six = numpy.zeros((6, 6), dtype=int)
        cls.nine = numpy.zeros((9, 9), dtype=int)
        cls.wrongBoard = numpy.zeros((5, 6), dtype=int)

        # Test variables for 4x4 board
        cls.hw = len(cls.four)
        cls.cells = []
        for i in range(cls.hw):
            for j in range(cls.hw):
                cls.cells.append((i, j))
        cls.constraints = [
            ((0, 0), (0, 1)), ((0, 0), (1, 0)), ((0, 0), (0, 2)), ((0, 0), (2, 0)),
            ((0, 0), (0, 3)), ((0, 0), (3, 0)), ((0, 1), (0, 0)), ((0, 1), (1, 1)),
            ((0, 1), (0, 2)), ((0, 1), (2, 1)), ((0, 1), (0, 3)), ((0, 1), (3, 1)),
            ((0, 2), (0, 0)), ((0, 2), (0, 1)), ((0, 2), (1, 2)), ((0, 2), (2, 2)),
            ((0, 2), (0, 3)), ((0, 2), (3, 2)), ((0, 3), (0, 0)), ((0, 3), (0, 1)),
            ((0, 3), (1, 3)), ((0, 3), (0, 2)), ((0, 3), (2, 3)), ((0, 3), (3, 3)),
            ((1, 0), (0, 0)), ((1, 0), (1, 1)), ((1, 0), (1, 2)), ((1, 0), (2, 0)),
            ((1, 0), (1, 3)), ((1, 0), (3, 0)), ((1, 1), (1, 0)), ((1, 1), (0, 1)),
            ((1, 1), (1, 2)), ((1, 1), (2, 1)), ((1, 1), (1, 3)), ((1, 1), (3, 1)),
            ((1, 2), (1, 0)), ((1, 2), (0, 2)), ((1, 2), (1, 1)), ((1, 2), (2, 2)),
            ((1, 2), (1, 3)), ((1, 2), (3, 2)), ((1, 3), (1, 0)), ((1, 3), (0, 3)),
            ((1, 3), (1, 1)), ((1, 3), (1, 2)), ((1, 3), (2, 3)), ((1, 3), (3, 3)),
            ((2, 0), (0, 0)), ((2, 0), (2, 1)), ((2, 0), (1, 0)), ((2, 0), (2, 2)),
            ((2, 0), (2, 3)), ((2, 0), (3, 0)), ((2, 1), (2, 0)), ((2, 1), (0, 1)),
            ((2, 1), (1, 1)), ((2, 1), (2, 2)), ((2, 1), (2, 3)), ((2, 1), (3, 1)),
            ((2, 2), (2, 0)), ((2, 2), (0, 2)), ((2, 2), (2, 1)), ((2, 2), (1, 2)),
            ((2, 2), (2, 3)), ((2, 2), (3, 2)), ((2, 3), (2, 0)), ((2, 3), (0, 3)),
            ((2, 3), (2, 1)), ((2, 3), (1, 3)), ((2, 3), (2, 2)), ((2, 3), (3, 3)),
            ((3, 0), (0, 0)), ((3, 0), (3, 1)), ((3, 0), (1, 0)), ((3, 0), (3, 2)),
            ((3, 0), (2, 0)), ((3, 0), (3, 3)), ((3, 1), (3, 0)), ((3, 1), (0, 1)),
            ((3, 1), (1, 1)), ((3, 1), (3, 2)), ((3, 1), (2, 1)), ((3, 1), (3, 3)),
            ((3, 2), (3, 0)), ((3, 2), (0, 2)), ((3, 2), (3, 1)), ((3, 2), (1, 2)),
            ((3, 2), (2, 2)), ((3, 2), (3, 3)), ((3, 3), (3, 0)), ((3, 3), (0, 3)),
            ((3, 3), (3, 1)), ((3, 3), (1, 3)), ((3, 3), (3, 2)), ((3, 3), (2, 3)),
            ((0, 0), (0, 1)), ((0, 0), (1, 0)), ((0, 0), (1, 1)), ((0, 1), (0, 0)),
            ((0, 1), (1, 0)), ((0, 1), (1, 1)), ((1, 0), (0, 0)), ((1, 0), (0, 1)),
            ((1, 0), (1, 1)), ((1, 1), (0, 0)), ((1, 1), (0, 1)), ((1, 1), (1, 0)),
            ((0, 2), (0, 3)), ((0, 2), (1, 2)), ((0, 2), (1, 3)), ((0, 3), (0, 2)),
            ((0, 3), (1, 2)), ((0, 3), (1, 3)), ((1, 2), (0, 2)), ((1, 2), (0, 3)),
            ((1, 2), (1, 3)), ((1, 3), (0, 2)), ((1, 3), (0, 3)), ((1, 3), (1, 2)),
            ((2, 0), (2, 1)), ((2, 0), (3, 0)), ((2, 0), (3, 1)), ((2, 1), (2, 0)),
            ((2, 1), (3, 0)), ((2, 1), (3, 1)), ((3, 0), (2, 0)), ((3, 0), (2, 1)),
            ((3, 0), (3, 1)), ((3, 1), (2, 0)), ((3, 1), (2, 1)), ((3, 1), (3, 0)),
            ((2, 2), (2, 3)), ((2, 2), (3, 2)), ((2, 2), (3, 3)), ((2, 3), (2, 2)),
            ((2, 3), (3, 2)), ((2, 3), (3, 3)), ((3, 2), (2, 2)), ((3, 2), (2, 3)),
            ((3, 2), (3, 3)), ((3, 3), (2, 2)), ((3, 3), (2, 3)), ((3, 3), (3, 2))
        ]
        cls.cell_domains = {
            (0, 0): {1, 2, 3, 4}, (0, 1): {1, 2, 3, 4}, (0, 2): {1, 2, 3, 4}, (0, 3): {1, 2, 3, 4},
            (1, 0): {1, 2, 3, 4}, (1, 1): {1, 2, 3, 4}, (1, 2): {1, 2, 3, 4}, (1, 3): {1, 2, 3, 4},
            (2, 0): {1, 2, 3, 4}, (2, 1): {1, 2, 3, 4}, (2, 2): {1, 2, 3, 4}, (2, 3): {1, 2, 3, 4},
            (3, 0): {1, 2, 3, 4}, (3, 1): {1, 2, 3, 4}, (3, 2): {1, 2, 3, 4}, (3, 3): {1, 2, 3, 4}
        }

    def test_arcs(self):
        self.assertEqual(arcs(self.four, self.hw), self.cells)
        self.assertEqual(len(arcs(self.six, 6)), 36)
        self.assertEqual(len(arcs(self.nine, 9)), 81)

    def test_find_constraints(self):
        self.assertEqual(find_constraints(self.wrongBoard, 5), TypeError)
        self.assertEqual(find_constraints(
            self.four, self.hw), self.constraints)

    def test_fill_domains(self):
        self.assertDictEqual(fill_domains(
            self.four, self.hw, self.cells, self.constraints), self.cell_domains)

    def test_find_neighbors(self):
        self.assertEqual(find_neighbors((0, 0), self.constraints), [
                         (0, 1), (1, 0), (0, 2), (2, 0), (0, 3), (3, 0), (1, 1)])

    def test_print_board(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        print_board(self.four, self.cells, self.hw)
        sys.stdout = sys.__stdout__
        self.assertEqual(
            print(capturedOutput.getvalue()),
            termcolor.cprint('0 0 0 0\n0 0 0 0\n0 0 0 0\n0 0 0 0', "red")
        )

    def test_select_unassigned_variable(self):
        self.assertEqual(select_unassigned_variable(
            self.cell_domains, self.hw), (0, 0))

    def test_consistent(self):
        false_board = numpy.array(self.four)
        false_board[0][0] = 1
        false_board[0][1] = 1
        self.assertFalse(consistent(false_board, self.constraints))
        self.assertTrue(consistent(self.four, self.constraints))

    def test_revise(self):
        domains_copy = self.cell_domains.copy()
        domains_copy[(0, 1)] = {1}
        self.assertTrue(revise((0, 0), (0, 1), domains_copy))
        self.assertFalse(revise((0, 0), (0, 1), self.cell_domains))


if __name__ == "__main__":
    unittest.main()
