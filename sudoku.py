import sys
import numpy
import termcolor
import time
from operator import itemgetter


def print_board(board, cells):
    """Print the sudoku board"""
    for j in range(9):
        for i in range(9):
            if (j, i) in cells:
                if board[j][i] > 0:
                    termcolor.cprint(board[j][i], "blue", end="")
                    print(' ', end="")
                else:
                    termcolor.cprint(board[j][i], "red", end="")
                    print(' ', end="")
            else:
                termcolor.cprint(board[j][i], "green", end="")
                print(' ', end="")
        if j < 8:
            print()


def find_neighbors(cell, CONSTRAINTS):
    """Find all neighboring cells to cell (for sudoku that is all neighbors that it cannot be the same as)"""
    neighbors = []
    for x, y in CONSTRAINTS:
        if x == cell:
            if not y in neighbors:
                neighbors.append(y)
        if y == cell:
            if not x in neighbors:
                neighbors.append(x)
    return neighbors


def select_unassigned_variable(assignment, domains, CONSTRAINTS):
    """Chooses a variable that has the least domains left"""
    for cell in domains:
        for i in range(1, 10):
            if len(domains[cell]) == i:
                return cell
    return None


def consistent(assignment, CONSTRAINTS):
    """Checks to see if an assignment is consistent."""
    for x, y in CONSTRAINTS:

        # Only consider arcs where both are assigned
        if assignment[x[0]][x[1]] == 0 or assignment[y[0]][y[1]] == 0:
            continue

        # If both have same value, then not consistent
        if assignment[x[0]][x[1]] == assignment[y[0]][y[1]]:
            return False

    # If nothing inconsistent, then assignment is consistent
    return True


def revise(x, y, domains):
    """Check if domains need to be modified when making variable x arc consistent with variable y"""
    revised = False
    new_set = set(domains[x])
    for n in domains[x]:
        if n in domains[y] and len(domains[y]) == 1:
            new_set.remove(n)
            revised = True
            continue
        count = 0
        for i in domains[y]:
            if n != i:
                count += 1
        if count == 0:
            new_set.remove(n)
            revised = True
    if revised:
        domains[x] = new_set
    return revised


def inference(var, domains, CONSTRAINTS):
    """AC3 algorithm to find inferences from an assignment"""
    queue = []
    if var != None:
        for a, b in CONSTRAINTS:
            if a is var:
                queue.append((a, b))
    else:
        for a, b in CONSTRAINTS:
            if len(domains[a]) > 0:
                queue.append((a, b))
    while (len(queue) != 0):
        (x, y) = queue.pop(0)
        if revise(x, y, domains):
            if len(domains[x]) == 0:
                return False
            neighbors = find_neighbors(x, CONSTRAINTS)
            for n in neighbors:
                if n != y:
                    queue.append((n, x))
    return True


def order_domain_values(var, domains, assignment, CONSTRAINTS):
    """Order domain values for variable depending on how many neighboring variables it will effect"""
    s = []
    neighbors = find_neighbors(var, CONSTRAINTS)
    for n in domains[var]:
        count = 0
        for v in neighbors:
            if assignment[v[0]][v[1]] > 0:
                continue
            for i in domains[v]:
                if n == i:
                    count += 1
        s.append((n, count))

    sorted_s = sorted(s, key=itemgetter(1))
    # Loop over sorted list and create new list of only values
    output = []
    for val in sorted_s:
        output.append(val[0])
    # Return new sorted list of values (no counts)
    return output


def backtrack(assignment, domains, CONSTRAINTS, cells):
    """Runs backtracking search to find an assignment."""
    # Print board has it completes
    print_board(assignment, cells)
    print("\033[9A")

    # Check if assignment is complete
    cells_check = 0
    for i in range(9):
        for j in range(9):
            if assignment[i][j] > 0:
                cells_check += 1
    if cells_check == 81:
        return assignment

    # Try a new variable
    var = select_unassigned_variable(assignment, domains, CONSTRAINTS)
    values = order_domain_values(var, domains, assignment, CONSTRAINTS)
    for val in values:
        new_assignment = assignment.copy()
        new_assignment[var[0]][var[1]] = val
        if consistent(new_assignment, CONSTRAINTS):
            new_domains = domains.copy()
            new_domains[var] = set()
            if inference(var, new_domains, CONSTRAINTS):
                for cell in new_domains:
                    if len(new_domains[cell]) == 1:
                        new_assignment[cell[0]][cell[1]] = new_domains[cell].pop()
            result = backtrack(new_assignment, new_domains, CONSTRAINTS, cells)
            if result is not None:
                return result

    return None


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python sudoku.py puzzle.csv")

    # Print solving has started
    print("Solving Sudoku:")

    # Load data
    puzzle = numpy.genfromtxt(
        sys.argv[1], delimiter=',', filling_values=0, dtype=int)

    # Arcs are the puzzle board cells that need filling
    cells = []
    for j in range(9):
        for i in range(9):
            if puzzle[j][i] == 0:
                cells.append((j, i))

    # Constraints for Sudoku game
    CONSTRAINTS = []
    for i in range(9):
        for j in range(9):
            start = (i, j)
            for n in range(9):
                if start != (i, n):
                    intermediate_row = (start, (i, n))
                    CONSTRAINTS.append(intermediate_row)
                if start != (n, j):
                    intermediate_col = (start, (n, j))
                    CONSTRAINTS.append(intermediate_col)

    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            for j in range(row, row + 3):
                for i in range(col, col + 3):
                    start = (j, i)
                    for r in range(row, row + 3):
                        for c in range(col, col + 3):
                            if (r, c) != start:
                                intermediate = (start, (r, c))
                                CONSTRAINTS.append(intermediate)

    # Domains are the numbers that could fill each cell
    # Some domains are empty to show the cell is already filled with a number
    cellDomains = {}
    for i in range(9):
        for j in range(9):
            if (i, j) in cells:
                c = (i, j)
                new_set = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
                neighbors = find_neighbors(c, CONSTRAINTS)
                for x in range(1, 10):
                    for n in neighbors:
                        if puzzle[n[0]][n[1]] == x:
                            new_set.discard(x)
                if len(new_set) == 1:
                    puzzle[i][j] = new_set.pop()
                cellDomains[c] = new_set
            else:
                cellDomains[(i, j)] = set()

    # Find solution and time it
    start = time.time()
    solution = backtrack(puzzle, cellDomains, CONSTRAINTS, cells)
    end = time.time()

    # Print how long it took
    print("\033[8B")
    s = round((end - start), 2)
    print(f"Took {s} s")


if __name__ == "__main__":
    main()
