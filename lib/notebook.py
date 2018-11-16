from inspect import getsource

from lib.utils import argmax, argmin
from IPython.display import HTML, display
from collections import Counter, defaultdict

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

import os, struct
import array
import time


#______________________________________________________________________________
# Magic Words


def pseudocode(algorithm):
    """Print the pseudocode for the given algorithm."""
    from urllib.request import urlopen
    from IPython.display import Markdown

    algorithm = algorithm.replace(' ', '-')
    url = "https://raw.githubusercontent.com/aimacode/aima-pseudocode/master/md/{}.md".format(algorithm)
    f = urlopen(url)
    md = f.read().decode('utf-8')
    md = md.split('\n', 1)[-1].strip()
    md = '#' + md
    return Markdown(md)


def psource(*functions):
    """Print the source code for the given function(s)."""
    source_code = '\n\n'.join(getsource(fn) for fn in functions)
    try:
        from pygments.formatters import HtmlFormatter
        from pygments.lexers import PythonLexer
        from pygments import highlight

        display(HTML(highlight(source_code, PythonLexer(), HtmlFormatter(full=True))))

    except ImportError:
        print(source_code)

# ______________________________________________________________________________
# MDP
def make_plot_grid_step_function(columns, rows, U_over_time):
    """ipywidgets interactive function supports single parameter as input.
    This function creates and return such a function by taking as input
    other parameters."""

    def plot_grid_step(iteration):
        data = U_over_time[iteration]
        data = defaultdict(lambda: 0, data)
        grid = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                current_row.append(data[(column, row)])
            grid.append(current_row)
        grid.reverse() # output like book
        fig = plt.imshow(grid, cmap=plt.cm.bwr, interpolation='nearest')

        plt.axis('off')
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)

        for col in range(len(grid)):
            for row in range(len(grid[0])):
                magic = grid[col][row]
                fig.axes.text(row, col, "{0:.2f}".format(magic), va='center', ha='center')

        plt.show()

    return plot_grid_step

def make_visualize(slider):
    """Takes an input a sliderand returns callback function
    for timer and animation."""

    def visualize_callback(Visualize, time_step):
        if Visualize is True:
            for i in range(slider.min, slider.max + 1):
                slider.value = i
                time.sleep(float(time_step))

    return visualize_callback

############################################################################################################

            #####################           Functions to assist plotting in ####################

############################################################################################################
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import lines
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage, AnnotationBbox)

from ipywidgets import interact
import ipywidgets as widgets
from IPython.display import display
import time
from lib.search import GraphProblem, romania_map

def show_map(graph_data, node_colors = None):
    G = nx.Graph(graph_data['graph_dict'])
    node_colors = node_colors or graph_data['node_colors']
    node_positions = graph_data['node_positions']
    node_label_pos = graph_data['node_label_positions']
    edge_weights= graph_data['edge_weights']
    
    # set the size of the plot
    plt.figure(figsize=(18,13))
    # draw the graph (both nodes and edges) with locations from romania_locations
    nx.draw(G, pos={k: node_positions[k] for k in G.nodes()},
            node_color=[node_colors[node] for node in G.nodes()], linewidths=0.3, edgecolors='k')

    # draw labels for nodes
    node_label_handles = nx.draw_networkx_labels(G, pos=node_label_pos, font_size=14)
    
    # add a white bounding box behind the node labels
    [label.set_bbox(dict(facecolor='white', edgecolor='none')) for label in node_label_handles.values()]

    # add edge lables to the graph
    nx.draw_networkx_edge_labels(G, pos=node_positions, edge_labels=edge_weights, font_size=14)
    
    # add a legend
    white_circle = lines.Line2D([], [], color="white", marker='o', markersize=15, markerfacecolor="white")
    orange_circle = lines.Line2D([], [], color="orange", marker='o', markersize=15, markerfacecolor="orange")
    red_circle = lines.Line2D([], [], color="red", marker='o', markersize=15, markerfacecolor="red")
    gray_circle = lines.Line2D([], [], color="gray", marker='o', markersize=15, markerfacecolor="gray")
    green_circle = lines.Line2D([], [], color="green", marker='o', markersize=15, markerfacecolor="green")
    plt.legend((white_circle, orange_circle, red_circle, gray_circle, green_circle),
               ('Un-explored', 'Frontier', 'Currently Exploring', 'Explored', 'Final Solution'),
               numpoints=1, prop={'size':16}, loc=(.8,.75))
    
    # show the plot. No need to use in notebooks. nx.draw will show the graph itself.
    plt.show()
    
## helper functions for visualisations
   
def final_path_colors(initial_node_colors, problem, solution):
    "Return a node_colors dict of the final path provided the problem and solution."
    
    # get initial node colors
    final_colors = dict(initial_node_colors)
    # color all the nodes in solution and starting node to green
    final_colors[problem.initial] = "green"
    for node in solution:
        final_colors[node] = "green"  
    return final_colors

def display_visual(graph_data, user_input, algorithm=None, problem=None):
    initial_node_colors = graph_data['node_colors']
    if user_input == False:
        def slider_callback(iteration):
            # don't show graph for the first time running the cell calling this function
            try:
                show_map(graph_data, node_colors=all_node_colors[iteration])
            except:
                pass
        def visualize_callback(Visualize):
            if Visualize is True:
                button.value = False
                
                global all_node_colors
                
                iterations, all_node_colors, node = algorithm(problem)
                solution = node.solution()
                all_node_colors.append(final_path_colors(all_node_colors[0], problem, solution))
                
                slider.max = len(all_node_colors) - 1
                
                for i in range(slider.max + 1):
                    slider.value = i
                     #time.sleep(.5)
        
        slider = widgets.IntSlider(min=0, max=1, step=1, value=0)
        slider_visual = widgets.interactive(slider_callback, iteration=slider)
        display(slider_visual)

        button = widgets.ToggleButton(value=False)
        button_visual = widgets.interactive(visualize_callback, Visualize=button)
        display(button_visual)
    
    if user_input == True:
        node_colors = dict(initial_node_colors)
        if isinstance(algorithm, dict):
            assert set(algorithm.keys()).issubset({"Breadth First Tree Search",
                                                       "Depth First Tree Search", 
                                                       "Breadth First Search", 
                                                       "Depth First Graph Search", 
                                                       "Best First Graph Search",
                                                       "Uniform Cost Search", 
                                                       "Depth Limited Search",
                                                       "Iterative Deepening Search",
                                                       "Greedy Best First Search",
                                                       "A-star Search",
                                                       "Recursive Best First Search"})

            algo_dropdown = widgets.Dropdown(description="Search algorithm: ",
                                             options=sorted(list(algorithm.keys())),
                                             value="Breadth First Tree Search")
            display(algo_dropdown)
        elif algorithm is None:
            print("No algorithm to run.")
            return 0
        
        def slider_callback(iteration):
            # don't show graph for the first time running the cell calling this function
            try:
                show_map(graph_data, node_colors=all_node_colors[iteration])
            except:
                pass
            
        def visualize_callback(Visualize):
            if Visualize is True:
                button.value = False
                
                problem = GraphProblem(start_dropdown.value, end_dropdown.value, romania_map)
                global all_node_colors
                
                user_algorithm = algorithm[algo_dropdown.value]
                
                iterations, all_node_colors, node = user_algorithm(problem)
                solution = node.solution()
                all_node_colors.append(final_path_colors(all_node_colors[0], problem, solution))

                slider.max = len(all_node_colors) - 1
                
                for i in range(slider.max + 1):
                    slider.value = i
                    #time.sleep(.5)
                         
        start_dropdown = widgets.Dropdown(description="Start city: ",
                                          options=sorted(list(node_colors.keys())), value="Arad")
        display(start_dropdown)

        end_dropdown = widgets.Dropdown(description="Goal city: ",
                                        options=sorted(list(node_colors.keys())), value="Fagaras")
        display(end_dropdown)
        
        button = widgets.ToggleButton(value=False)
        button_visual = widgets.interactive(visualize_callback, Visualize=button)
        display(button_visual)
        
        slider = widgets.IntSlider(min=0, max=1, step=1, value=0)
        slider_visual = widgets.interactive(slider_callback, iteration=slider)
        display(slider_visual)

# Function to plot NQueensCSP in csp.py and NQueensProblem in search.py
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
