#!/usr/bin/env python3
# Useful imports

from __future__ import division

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import copy
from nose.tools import ok_, assert_equal, assert_almost_equal
from lib.grid import MDPGrid, generate_mdp_plot

n = 3
goal = (2,2)
obstacles = [(0,1)]

# Create grid for plotting
g = MDPGrid(n,n)
axes = g.draw()
# Draw goal and obstacle cells
g.draw_cell_circle(axes, goal, color='g')
for ob in obstacles:
    g.draw_cell_circle(axes, ob, color='k')



