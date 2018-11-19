from inspect import getsource
from IPython.display import HTML, display
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
