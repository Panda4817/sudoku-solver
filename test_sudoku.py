import unittest
import numpy
from sudoku import *


class SudokuTestCase(unittest.TestCase):

    def __init__(self):
        self.puzzle = numpy.genfromtxt(
            'empty.csv', delimiter=',', filling_values=0, dtype=int)
        self.hw = len(puzzle)
    
    