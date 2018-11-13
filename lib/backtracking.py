from __future__ import print_function

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
            restore_domains(csp, var)
    return None

#--------------------------------------------------------------------------------------------#
# INFERENCE
def inference(csp, var, assignment):
    """ Do inference based on newest assignment. """
    if csp.fc:
        """ One option is to use forward_checking """
        return forward_checking(csp, var, assignment)
    # If we do not implement an inference algorithm, just return that everything is ok.
    # If everything went ok after inference, return True as well.
    return True

def forward_checking(csp, var, assignment):
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


def restore_domains(csp, var):
    """ Restores the domains that a variable var pruned when doing inference """
    for (B, b) in csp.pruned[var]:
        csp.curr_domains[B].append(b)
    csp.pruned[var] = []

#--------------------------------------------------------------------------------------------#
# SELECT_UNASSIGNED_VARIABLE
def select_unassigned_variable(assignment, csp):
    """ Select the variable to work on next. """
    # First unassigned variable
    for v in csp.vars:
        if v not in assignment:
            return v
        
#--------------------------------------------------------------------------------------------#
# ORDER_DOMAIN_VALUES
def order_domain_values(var, assignment, csp):
    """ Decide what order to consider the domain variables. """
    # Just give the domain as it is, default is in order.
    domain = csp.curr_domains[var]
    return domain