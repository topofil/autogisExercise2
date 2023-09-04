#!/usr/bin/env python3


"""Load the code-cells of a jupyter notebook."""

import re
import types

import nbformat


def import_notebook(path):
    notebook = nbformat.read(str(path), as_version=nbformat.NO_CONVERT)

    global _plot
    _plot = 1  # start counting fresh in every notebook

    namespace = {}
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            try:
                code_cell = _keep_plots(cell["source"])
                exec(code_cell, namespace)
            except Exception:  # ignore any cell that has any error
                pass

    del namespace["__builtins__"]
    namespace = types.SimpleNamespace(**namespace)
    return namespace


_RE_LINE_ENDING_IN_PLOT = re.compile(
    r'^(?P<indent>\s*)(?P<code>.*\.plot\(\))$'
)


_plot = 1


def _keep_plots(code_cell):
    """
    Replaces lines that end in plot() so plots would be preserved

    This is a very crude hack, and we have to find better ways of
    capturing plots in notebooks
    """
    global _plot

    code_cell = code_cell.splitlines()
    output = []
    for line in code_cell:
        if match := _RE_LINE_ENDING_IN_PLOT.match(line):
            line = f"{match['indent']}_PLOT_{_plot} = {match['code']}"
            _plot += 1
        output.append(line)

    return "\n".join(output)
