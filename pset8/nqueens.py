from __future__ import print_function
import time

# CSP Backtracking Search
def backtracking_search(csp, fc=False):
    """Set up to do recursive backtracking search. Allow the following options:
    fc  - If true, use Forward Checking
    """
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
            # Unprune domains
            # Reset the curr_domain to be the full original domain
            #csp.curr_domains[var] = csp.domains[var][:]

            # Restore prunings from previous value of var
            for (B, b) in csp.pruned[var]:
                csp.curr_domains[B].append(b)
            csp.pruned[var] = []
    return None

def inference(csp, var, assignment):
    "Do forward checking (current domain reduction) for this assignment."
    if csp.fc:
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
    # If we do not implement an inference algorithm, just return that everything is ok.
    # If everything went ok after inference, return True as well.
    return True

def select_unassigned_variable(assignment, csp):
    "Select the variable to work on next.  Find"
    # First unassigned variable
    for v in csp.vars:
        if v not in assignment:
            return v

def order_domain_values(var, assignment, csp):
    "Decide what order to consider the domain variables."
    # Just give the domain as it is, default is in order.
    domain = csp.curr_domains[var]
    return domain
        
# n-Queens Problem
def queen_constraint(A, a, B, b):
    """Constraint is satisfied (true) if A, B are really the same variable,
    or if they are not in the same row, down diagonal, or up diagonal."""
    return A == B or (a != b and A + a != B + b and A - a != B - b)

def all_different(L):
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
        # {A:[(B, b1), (B, b2), (C, c3), ...]}
        self.pruned = {var:[] for var in self.vars}
        self.constraints = queen_constraint

    def is_consistent(self, var, val, assignment):
        """ Is consistent? """
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
        """Add {var: val} to assignment; Discard the old value if any.
        Do bookkeeping for curr_domains."""
        assignment[var] = val
                
    def unassign(self, var, assignment):
        """Remove {var: val} from assignment; that is backtrack.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]
            
    def prune_domain(self, var, val):
        """ Apply arc-consistency.
        Wheneever a variable X is assigned, the forward-checking processs establishes arc consistency
        for it: for each unassgined variable Y that is connected to X by a constraint, delete from Y's domain
        any value that is inconsistent with the value chosen for X.
        Return:
            - Whether the pruning of the domains resulted in an empty domain or not, which indicates if the 
            var=val assignment is arc-consistent.
        """
        old_domain = self.domain.copy()
        self.domain[var] = {val}
        for x in range(self.N):
            if x == var:
                continue
            for v in self.domain[x]:
                # Constraint: alldifferent(q)
                if v == val:
                    self.domain[x] = self.domain[x] - {v}
                    self.consistency_checks = self.consistency_checks + 1
                    if len(self.domain[x]) == 0:
                        return old_domain
                # Constraint: alldifferent(q[i] + i)
                if v + x == val + var:
                    self.domain[x] = self.domain[x] - {v}
                    self.consistency_checks = self.consistency_checks + 1
                    if len(self.domain[x]) == 0:
                        return old_domain
                # Constraint: alldifferent(q[i] - i)
                if v - x == val - var:
                    self.domain[x] = self.domain[x] - {v}
                    self.consistency_checks = self.consistency_checks + 1
                    if len(self.domain[x]) == 0:
                        return old_domain
        return old_domain
    
def display(csp, assignment):
    "Print the queens"
    n = len(csp.vars)
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

    start_time = time.time()
    solution = backtracking_search(n_queens, fc=True)
    end_time = time.time()
    print(solution)
    print(end_time - start_time)
    display(n_queens, solution)
