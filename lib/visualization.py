import copy
from lib.n_queens_csp import *
from lib.notebook import  plot_NQueens

# Hide warnings in the matplotlib sections
import warnings
warnings.filterwarnings("ignore")

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import ipywidgets as widgets
from IPython.display import display

## Wrapper around NQueensCSP to store partial assignments and visualize the inner workings of the algorithm.
class InstruCSP(NQueensCSP):
    
    def __init__(self, N):
        super().__init__(N)
        self.assignment_history = []
        
    def is_consistent(self, var, val, assignment):
        attempt_assignment = {var: val}
        attempt_assignment.update(assignment)
        if len(self.assignment_history) > 0:
            # Second or older assignemnt, we can re-use the pruned domains, they will be overwritten
            # if is_consistent returns false, as we won't get into track_pruned_domains_for_display
            self.assignment_history.append([copy.deepcopy(attempt_assignment), self.assignment_history[-1][1]])
        else:
            # First assignment, therefore there are no pruned domains...
            self.assignment_history.append([copy.deepcopy(attempt_assignment), None])
        
        #runed_domains = copy.deepcopy(self.domains)
        #or var, val in self.curr_domains:
        #   pruned_domains[var].remove(val)
        #elf.pruned_domains_history.append[pruned_domains]
        return super().is_consistent(var, val, assignment)
        
    #def assign(self, var, val, assignment):
        #super().assign(var, val, assignment)
        #self.assignment_history.append(copy.deepcopy(assignment))
        
    def track_pruned_domain_for_display(self):
        pruned_domains = copy.deepcopy(self.domains)
        for var, values in self.curr_domains.items():
            for val in values:
                pruned_domains[var].remove(val)
        self.assignment_history[-1] = [self.assignment_history[-1][0], pruned_domains]
        return super().track_pruned_domain_for_display()
    
    def unassign(self, var, assignment):
        super().unassign(var, assignment)
        pruned_domains = copy.deepcopy(self.domains)
        for var, values in self.curr_domains.items():
            for val in values:
                pruned_domains[var].remove(val)
        self.assignment_history.append([copy.deepcopy(assignment), pruned_domains])
        
        #runed_domains = copy.deepcopy(self.domains)
        #or var, val in self.curr_domains:
        #   pruned_domains[var].remove(val)
        #elf.pruned_domains_history.append[pruned_domains]
        
# Create the actual wrapper.
def make_instru(csp):
    return InstruCSP(len(csp.variables))

## FOR VISUALIZATION
def label_queen_conflicts(assignment,grid):
    ''' Mark grid with queens that are under conflict. '''
    for col, row in assignment.items(): # check each queen for conflict
        conflicts = {temp_col: temp_row for temp_col, temp_row in assignment.items() if (temp_row == row and temp_col != col or (temp_row+temp_col == row+col and temp_col != col) or (temp_row-temp_col == row-col and temp_col != col))}
        
        # Place a 3 in positions where this is a conflict
        for col, row in conflicts.items():
            grid[row][col] = 3

    return grid

def label_empty_domains(pruned_domains,grid):
    ''' Mark grid with queens that are under conflict. '''
    for var, values in pruned_domains.items():
        if len(values) == len(grid):
            # Place a 3 in positions where this is a conflict
            for val in values:
                grid[val][var] = 2

    return grid


def make_plot_board_step_function(instru_csp):
    '''ipywidgets interactive function supports
       single parameter as input. This function
       creates and return such a function by taking
       in input other parameters.
    '''
    n = len(instru_csp.variables) 
    
    def plot_board_step(iteration):
        ''' Add Queens to the Board.'''
        data = instru_csp.assignment_history[iteration]
        #pruned_domains = instru_csp.pruned_domains_history[iteration]
        
        grid = [[(col+row+1)%2 for col in range(n)] for row in range(n)]
        grid = label_queen_conflicts(dict(data[0]), grid) # Update grid with conflict labels.
        grid = label_empty_domains(dict(data[1]), grid) # Update grid with conflict labels.
        # color map of fixed colors
        cmap = matplotlib.colors.ListedColormap(['white','black','yellow','red'])
        bounds=[0,1,2,3,4] # 0 for white 1 for black 2 onwards for conflict labels (yellow for domain empty, red for conflict).
        norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
        
        plot_NQueens(data[0], data[1], n, grid, cmap, norm)
    
    return plot_board_step

def make_visualize(slider, visualize_button):
    ''' Takes as input a slider and returns 
        callback function for timer and animation
    '''
    
    def visualize_callback(Visualize, time_step):
        i = slider.min
        while Visualize is True and i < slider.max + 1:
            slider.value = i
            i += 1
            time.sleep(float(time_step))      
    
    return visualize_callback

def display_nqueens(backtracking_instru_queen, result):
    backtrack_queen_step = make_plot_board_step_function(backtracking_instru_queen) # Step Function for Widgets

    iteration_slider = widgets.IntSlider(min=0, max=len(backtracking_instru_queen.assignment_history)-1, step=1, value=0)
    w = widgets.interactive(backtrack_queen_step,iteration=iteration_slider)
    display(w)

    #visualize_button = widgets.ToggleButton(description = "Visualize", value = False)
    #visualize_callback = make_visualize(iteration_slider, visualize_button)

    #time_select = widgets.ToggleButtons(description='Extra Delay:', options=['0', '0.1', '0.2', '0.5', '0.7', '1.0'])

    #a = widgets.interactive(visualize_callback, Visualize = visualize_button, time_step = time_select)
    #display(a)