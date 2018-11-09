from __future__ import print_function
import time

def backtracking_search(csp, fc=False):
    """ Backtracking search as detailed in Fig. 6.5 of AIMA book. """
    csp.fc = fc
    return backtrack({}, csp)

def backtrack(assignment, csp):
    """Search for a consistent assignment for the csp.
    Each recursive call chooses a variable, and considers values for it."""
    # If assignment is complete then return assignment.
    if len(assignment) == len(csp.vars):
        return assignment
    # Select an unassigned variable.
    var = select_unassigned_variable(assignment, csp)
    # Loop over the domain of the current variable.
    for val in order_domain_values(var, assignment, csp):
        # If value is consistent with assignment, continue.
        if csp.is_consistent(var, val, assignment) == True:
            # Assign the value to the variable.
            csp.assign(var, val, assignment)
            # If we do not use forward checking, we are good!
            # If we do forward checking, prune domains, and continue only if no domain is empty.
            if inference(csp, var, assignment) == True:
                # Calculate next result (recursive call).
                result = backtrack(assignment, csp)
                if result is not None:
                    return result
        # If we have a conflict, unassign.
        # If we use forward checking, restore domains pruned by this assignment var=val.
        csp.unassign(var, assignment)
        if csp.fc:
            # Restore prunings from previous value of var
            csp.restore_domains(var)
    return None

def inference(csp, var, assignment):
    """ Do inference based on newest assignment. """
    if csp.fc:
        """ One option is to use forward_checking """
        return csp.forward_checking(csp, var, assignment)
    # If we do not implement an inference algorithm, just return that everything is ok.
    # If everything went ok after inference, return True as well.
    return True

def select_unassigned_variable(assignment, csp):
    """ Select the variable to work on next. """
    # First unassigned variable
    for v in csp.vars:
        if v not in assignment:
            return v

def order_domain_values(var, assignment, csp):
    """ Decide what order to consider the domain variables. """
    # Just give the domain as it is, default is in order.
    domain = csp.curr_domains[var]
    return domain

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

    def forward_checking(self, csp, var, assignment):
        """ Prunes the domains by applying arc-consistency between a var and its neighbors """
        # Get val.
        val = assignment[var]
        # Loop over domains of yet not assigned variables.
        for B in csp.vars:
                    if B not in assignment:
                        # Loop over values in the current domain of B.
                        for b in csp.curr_domains[B]:
                            # If B = b is not consistent with var = val.
                            if not csp.constraints(var, val, B, b):
                                # Remove b from B's domain.
                                csp.curr_domains[B].remove(b)
                                # Store pruned value from B's domain, used to restore domain
                                # in case of backtracking.
                                csp.pruned[var].append((B, b))
                                # We got an empty domain!
                                if len(csp.curr_domains[B]) == 0:
                                    # var = val is not arc-consistent!
                                    return False
        return True

    def restore_domains(self, var):
        """ Restores the domains that a variable var pruned when doing inference """
        for (B, b) in self.pruned[var]:
            self.curr_domains[B].append(b)
        self.pruned[var] = []


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

