# ______________________________________________________________________________
# Constraint Propagation with AC-3
import lib.csp
import time
import matplotlib.pyplot as plt

def AC3(csp, queue=None, removals=None):
    """[Figure 6.3]"""
    if queue is None:
        queue = [(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]]
    csp.support_pruning()
    while queue:
        (Xi, Xj) = queue.pop()
        if revise(csp, Xi, Xj, removals):
            if not csp.curr_domains[Xi]:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    return True

def revise(csp, Xi, Xj, removals):
    """Return true if we remove a value."""
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised

def AC1(csp, queue=None, removals=None):
    """[Figure 6.3]"""
    if queue is None:
        queue = [(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]]
    csp.support_pruning()
    while queue:
        (Xi, Xj) = queue.pop()
        revise(csp, Xi, Xj, removals); revise(csp, Xj, Xi, removals)
    return True

def implementAC1(e):
    counter = 0
    start_time = time.time()
    elast = dict()
    while True:
        check =  False
        AC1(e);
        counter += 1
        for i in range(80):
            if i not in e.infer_assignment():
                check = True
                break
        if counter != 0 and check:
            if elast == e.infer_assignment():
                print()
                e.display(e.infer_assignment())
                print('\nSolution not found after %d iterations'%counter)
                print('time taken is %f seconds'%(time.time()-start_time))
                break
        if not check:
            print()
            e.display(e.infer_assignment())
            print('\nSolution found in %d iterations'%counter)
            print('time taken to solve is %f seconds'%(time.time()-start_time))
            break
        elast = e.infer_assignment().copy()

def implementAC3(e):
    counter = 0
    start_time = time.time()
    elast = dict()
    while True:
        check =  False
        AC3(e);
        counter += 1
        for i in range(80):
            if i not in e.infer_assignment():
                check = True
                break
        if counter != 0 and check:
            if elast == e.infer_assignment():
                print()
                e.display(e.infer_assignment())
                print('\nSolution not found after %d iterations'%counter)
                print('time taken is %f seconds'%(time.time()-start_time))
                break
        if not check:
            print()
            e.display(e.infer_assignment())
            print('\nSolution found in %d iterations'%counter)
            print('time taken to solve is %f seconds'%(time.time()-start_time))
            break
        elast = e.infer_assignment().copy()
