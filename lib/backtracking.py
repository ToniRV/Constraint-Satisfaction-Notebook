from __future__ import print_function
from lib.utils import argmin_random_tie, count, first
from lib.constraint_propagation import AC3

#--------------------------------------------------------------------------------------------#
# INFERENCE
def no_inference(csp, var, assignment, removals):
    """ If we do not implement an inference algorithm, just return that everything is ok."""
    return True

def forward_checking(csp, var, assignment, removals):
    """ Prunes the domains by applying arc-consistency between a var and its neighbors """
    #from IPython.core.debugger import set_trace
    #set_trace()
    csp.support_pruning()
    # Get val.
    val = assignment[var]
    # Loop over domains of yet not assigned variables neighbors of var.
    for B in csp.neighbors[var]:
        if B not in assignment:
            # Loop over values in the current domain of B.
            for b in csp.curr_domains[B][:]: # Iterate over a copy of the list (thereby the [:])
                # If B = b is not consistent with var = val.
                if not csp.constraints(var, val, B, b):
                    csp.prune(B, b, removals)
                    # We got an empty domain!
                    if len(csp.curr_domains[B]) == 0:
                        # var = val is not arc-consistent!
                        return False
    return True

def restore_domains(csp, var):
    """ Restores the domains that a variable var pruned when doing inference """
    for (B, b) in csp.pruned[var]:
        csp.curr_domains[B].append(b)
    csp.pruned[var] = []
    
def mac(csp, var, assignment, removals):
    """Maintain arc consistency."""
    return AC3(csp, [(X, var) for X in csp.neighbors[var]], removals)

#--------------------------------------------------------------------------------------------#
# SELECT_UNASSIGNED_VARIABLE
def first_unassigned_variable(assignment, csp):
    """ Select the variable to work on next. """ 
    # First unassigned variable
    return first([var for var in csp.variables if var not in assignment])

def mrv(assignment, csp):
    """Minimum-remaining-values heuristic."""
    return argmin_random_tie(
        [var for var in csp.variables if var not in assignment],
        key=lambda var: num_legal_values(csp, var, assignment))

def num_legal_values(csp, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        return count(csp.nconflicts(var, val, assignment) == 0
                     for val in csp.domains[var])
        
#--------------------------------------------------------------------------------------------#
# ORDER_DOMAIN_VALUES
def unordered_domain_values(var, assignment, csp):
    """The default value order."""
    return csp.choices(var)


def lcv(var, assignment, csp):
    """Least-constraining-values heuristic."""
    return sorted(csp.choices(var),
                  key=lambda val: csp.nconflicts(var, val, assignment))


#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#
# Backtracking Algorithm
def backtracking_search(csp, select_unassigned_variable = first_unassigned_variable,
                        order_domain_values = unordered_domain_values,
                        inference = no_inference):
    """ Backtracking search as detailed in Fig. 6.5 of AIMA book. """
    
    def backtrack(assignment, csp):
        """Search for a consistent assignment for the csp.
        Each recursive call chooses a variable, and considers values for it."""
        # If assignment is complete then return assignment.
        if len(assignment) == len(csp.variables):
            return assignment
        # Select an unassigned variable.
        var = select_unassigned_variable(assignment, csp)
        # Loop over the domain of the current variable.
        for val in order_domain_values(var, assignment, csp):
            # If value is consistent with assignment, continue.
            if csp.is_consistent(var, val, assignment):
                # Assign the value to the variable.
                csp.assign(var, val, assignment)
                # If we do not use forward checking, we are good!
                # If we do forward checking, prune domains, and continue only if no domain is empty.
                removals = csp.suppose(var, val)
                infer = inference(csp, var, assignment, removals)
                csp.track_pruned_domain_for_display()
                if infer:
                    # Calculate next result (recursive call).
                    result = backtrack(assignment, csp)
                    if result is not None:
                        return result
                csp.restore(removals)
                # If we have a conflict, unassign.
                # If we use forward checking, restore domains pruned by this assignment var=val.
                csp.unassign(var, assignment) # could be done outside the for loop...
        return None
    
    # Start backtracking
    result = backtrack({}, csp)
    assert result is None or csp.goal_test(result)
    return result

