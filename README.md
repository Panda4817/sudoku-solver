# Python Sudoku Solver

I used backtracking search algorithm with some optimization heuristics to solve any valid sudoku boards. The board is loaded from a csv file. It will print out the board as it is being solved and afterwards print out the number of seconds it took to solve it.

## Requirements

Numpy, termcolor and pyfiglet.

## Usage

Run `python sudoku.py path_to_puzzle_board.csv`. Example puzzle boards are in the directory `example_puzzles`.