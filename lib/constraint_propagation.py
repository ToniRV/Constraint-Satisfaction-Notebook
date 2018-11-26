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

def implementAC1(e,pr=True):
    counter = 0
    start_time = time.time()
    elast = dict()
    done = False
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
                t = time.time()-start_time
                if pr:
                    print()
                    e.display(e.infer_assignment())
                    print('\nSolution not found after %d iterations'%counter)
                    print('time taken is %f seconds'%t)
                break
        if not check:
            t = time.time()-start_time
            if pr:
                print()
                e.display(e.infer_assignment())
                print('\nSolution found in %d iterations'%counter)
                print('time taken to solve is %f seconds'%t)
            done = True
            break
        elast = e.infer_assignment().copy()
    return t, done

def implementAC3(e,pr=True):
    counter = 0
    start_time = time.time()
    elast = dict()
    done = False
    while True:
        check = False
        AC3(e);
        counter += 1
        for i in range(80):
            if i not in e.infer_assignment():
                check = True
                break
        if counter != 0 and check:
            if elast == e.infer_assignment():
                t = time.time()-start_time
                if pr:
                    print()
                    e.display(e.infer_assignment())
                    print('\nSolution not found')
                    print('time taken is %f seconds'%t)                
                break
        if not check:
            t = time.time()-start_time
            if pr:
                print()
                e.display(e.infer_assignment())
                print('time taken to solve is %f seconds'%t)
            done = True
            break             
        elast = e.infer_assignment().copy()
    return t, done