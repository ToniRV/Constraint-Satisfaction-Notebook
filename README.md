# Constraint-Satisfaction-Notebook
Example lecture for Constraint Satisfaction Problems in an interactive jupyter notebook style.

-- Let us look first at already coded examples, there are many: just add the links here:
https://www.geeksforgeeks.org/sudoku-backtracking-7/
https://www.geeksforgeeks.org/m-coloring-problem-backtracking-5/
http://www.angusj.com/sudoku/hints.php


These slides look very similar to what Brian Williams uses:
http://gki.informatik.uni-freiburg.de/teaching/ss12/csp/csp04-handout.pdf


Norvig’s
http://norvig.com/sudoku.html


https://en.wikipedia.org/wiki/Sudoku_solving_algorithms


## Utility functions:
1- Plotting the Sudoku
2- Representation of State and Domains

## Algorithms:
1- Extract common functions that we can use for all algorithms.
2- 

## Installation
Heavily recommended to use a virtual environment to use this setup.
You can do that by for example using virtualenv and virtualenvwrapper.

Install pip:

If in Mac, do (assuming you installed brew, which you should...):
```
brew install pip
```

If in Linux:
```
sudo apt-get install pip
```

Install virtualenv:
```
pip install virtualenv
```

Install virtualenvwrapper:
```
pip install virtualenvwrapper
```

Now, let's clone this repo and install the necessary requirements.
```
git clone git@github.com:ToniRV/Constraint-Satisfaction-Notebook.git csp_notebook
```
Or if you don't want to use SSH or you don't have it setup:
```
git clone https://github.com/ToniRV/Constraint-Satisfaction-Notebook.git csp_notebook
```

cd csp_notebook
mkvirtualenv csp_notebook --python=/usr/local/bin/python3 -r requirements.txt
```

Finally, activate your virtual environment:
```
workon csp_notebook
```

You are ready to go!
```
jupyter notebook CSPs.ipynb
```
