from __future__ import print_function
import time
from backtracking import backtracking_search

def queen_constraint(A, a, B, b):
    """Constraint is satisfied (true) if A, B are really the same variable,
    or if they are not in the same row, down diagonal, or up diagonal."""
    return A == B or (a != b and A + a != B + b and A - a != B - b)

def all_different(L):
    """ Utility function to check that all values in the list are different """
    isinstance(L, list)
    result = set()
    for value in L:
        if value not in result:
            result.add(value)
        else:
            return False
    return True

class NQueensCSP():
    """Make a CSP for the nQueens problem for search with backtracking """

    def __init__(self, n):
        """Initialize data structures for n Queens."""
        # Indices of variables in the problem.
        self.vars = list(range(n))
        # Initial domains of the variables.
        self.domains = {var:list(range(n)) for var in self.vars}
        # Current domains of the variables after pruning, only used for forward checking.
        self.curr_domains = {var:list(range(n)) for var in self.vars}
        # Pruned B=b pairs due to a given A=a assignment.
        # Used to restore domains if an assignment gets backtracked.
        # {A:[(B, b1), (B, b2), (C, c3)], B: [(C, c1)], ...}
        self.pruned = {var:[] for var in self.vars}
        # Store constraints that a pair of variables should satisfy.
        self.constraints = queen_constraint

    def is_consistent(self, var, val, assignment):
        """ Check if the attempted var = val assignment is consistent with current assignment """
        # Add var = val in the list of assignments as a first attempt.
        # Slow because we are copying, but perfect for pedagogical purposes.
        attempt_assignment = {var: val}
        attempt_assignment.update(assignment)
        # Check for same column constraint is implicit in formulation.
        # Check for same row constraint:
        c_row = all_different(attempt_assignment.values())
        # Check for same diagonal constraint:
        diag_1 = [key + value for key, value in attempt_assignment.items()]
        diag_2 = [key - value for key, value in attempt_assignment.items()]
        c_diag_1 = all_different(diag_1)
        c_diag_2 = all_different(diag_2)

        return c_row and c_diag_1 and c_diag_2

    def assign(self, var, val, assignment):
        """ Add {var: val} to assignment, discards the old value if any. """
        assignment[var] = val

    def unassign(self, var, assignment):
        """ Remove {var: val} from assignment; that is backtrack. """
        if var in assignment:
            del assignment[var]


    def display(self, assignment):
        """ Print the queens """
        n = len(self.vars)
        for val in range(n):
            for var in range(n):
                if assignment.get(var,'') == val:
                    ch ='Q'
                elif (var + val) % 2 == 0:
                    ch = '.'
                else:
                    ch = '-'
                print(ch, end=" "),
            print('    ')

if __name__== "__main__":
    # Solve n queens.
    n_queens = NQueensCSP(15)

    # Backtracking
    start_time = time.time()
    solution = backtracking_search(n_queens, fc=False)
    end_time = time.time()
    print(solution)
    print(end_time - start_time)
    n_queens.display(solution)

    # Backtracking with forward checking
    start_time = time.time()
    solution = backtracking_search(n_queens, fc=True)
    end_time = time.time()
    print(solution)
    print(end_time - start_time)
    n_queens.display(solution)