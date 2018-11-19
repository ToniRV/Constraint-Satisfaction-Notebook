import copy
import time
from lib.n_queens_csp import *

# Hide warnings in the matplotlib sections
import warnings
warnings.filterwarnings("ignore")

import numpy as np
from PIL import Image
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import lines
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage, AnnotationBbox)

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
        return super().is_consistent(var, val, assignment)

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

# Create the actual wrapper.
def make_instru(csp):
    return InstruCSP(len(csp.variables))

## For visualization

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

    # TODO solve the issue with the Visualize button not stopping the display.
    #visualize_button = widgets.ToggleButton(description = "Visualize", value = False)
    #visualize_callback = make_visualize(iteration_slider, visualize_button)

    #time_select = widgets.ToggleButtons(description='Extra Delay:', options=['0', '0.1', '0.2', '0.5', '0.7', '1.0'])

    #a = widgets.interactive(visualize_callback, Visualize = visualize_button, time_step = time_select)
    #display(a)

## For nqueens visualization

# Function to plot NQueensCSP
def plot_NQueens(partial_assignment, pruned_domains = None, n = -1, grid = None, cmap = 'binary', norm = None):
    ''' Plot a checkerboard with Queens placed on it.
        partial_assignment is a dict or a list specifying the rows of the Queens on the board on each column.
        n is the size of the board, if n is less than 0, then we assume the board is the size of the partial_assignment.
    '''
    if n <= 0:
        n = len(partial_assignment)

    fig_size = 7
    fig = plt.figure(figsize=(fig_size, fig_size))
    ax = fig.add_subplot(111)
    ax.set_title('{} Queens'.format(n))

    # Generate the checkerboard.
    if grid == None:
        board = np.array([2 * int((i + j) % 2) for j in range(n) for i in range(n)]).reshape((n, n))
        plt.imshow(board, cmap=cmap, interpolation='nearest')
    else:
        if norm == None:
            plt.imshow(grid, cmap=cmap, interpolation='nearest')
        else:
            plt.imshow(grid, cmap=cmap, interpolation='nearest', norm=norm)

    # Get Queen image.
    im = Image.open('images/queen_s.png')
    im = np.array(im).astype(np.float) / 255
    im_x = Image.open('images/x.png')
    im_x = np.array(im_x).astype(np.float) / 255

    # Internal function to plot the image of a queen inside the board.
    def plot_image_on_axis(ax, im, zoom, x, y):
        ''' Function to plot an image 'im' in an axis 'ax' at x, y coords'''
        off_im = OffsetImage(im, zoom=zoom)
        off_im.image.axes = ax
        ab = AnnotationBbox(off_im, [k, v],
                            xybox=(0, 0),
                            frameon=False,
                            xycoords='data',
                            boxcoords="offset points",
                            pad=0.3,
                            arrowprops=dict(arrowstyle="->"))
        ax.add_artist(ab)

    # If NQueensProblem gives a partial_assignment as a dict
    if isinstance(partial_assignment, dict):
        for (k, v) in partial_assignment.items():
            plot_image_on_axis(ax, im, 1/n, k, v)
        if pruned_domains:
            for (k, values) in pruned_domains.items():
                for v in values:
                    plot_image_on_axis(ax, im_x, 0.5*1/n, k, v)
    # If NQueensProblem gives a partial_assignment as a list
    elif isinstance(partial_assignment, list):
        for (k, v) in enumerate(partial_assignment):
            plot_image_on_axis(ax, im, 1/n, k, v)
    fig.tight_layout()
    plt.show()
