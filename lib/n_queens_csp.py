from __future__ import print_function
import time
import copy
from lib.backtracking import backtracking_search
from lib.csp import CSP

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

class NQueensCSP(CSP):
    """Make a CSP for the nQueens problem for search with backtracking """

    def __init__(self, n):
        """Initialize data structures for n Queens."""
        # Indices of variables in the problem.
        variables = list(range(n))
        # Initial domains of the variables.
        domains = {var:list(range(n)) for var in variables}
        # What are the neighbors of a given var, can include itself.
        neighbors = {var:list(range(n)) for var in variables}
        
        CSP.__init__(self, variables, domains, neighbors, queen_constraint)
    

    def is_consistent(self, var, val, assignment):
        """ Check if the attempted var = val assignment is consistent with current assignment """
        # Add var = val in the list of assignments as a first attempt.
        # Slow because we are copying, but perfect for pedagogical purposes.
        attempt_assignment = copy.deepcopy(assignment)
        if var != None and val != None:
            attempt_assignment.update({var: val})
        # Check for same column constraint is implicit in formulation.
        # Check for same row constraint:
        c_row = all_different(attempt_assignment.values())
        # Check for same diagonal constraint:
        diag_1 = [key + value for key, value in attempt_assignment.items()]
        diag_2 = [key - value for key, value in attempt_assignment.items()]
        c_diag_1 = all_different(diag_1)
        c_diag_2 = all_different(diag_2)

        return c_row and c_diag_1 and c_diag_2
            
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