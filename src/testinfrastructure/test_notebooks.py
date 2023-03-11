import re
import sys
import os
import argparse

from glob import glob
from pathlib import Path
from functools import reduce
from nbconvert.preprocessors import ExecutePreprocessor
from jupytext import jupytext
from typing import List


def run_nbnode(nb, run_path):
    # from
    # https://www.blog.pythonlibrary.org/2018/10/16/testing-jupyter-notebooks/
    proc = ExecutePreprocessor(timeout=600, kernel_name='python3')
    proc.allow_errors = True

    proc.preprocess(nb, {'metadata': {'path': run_path}})

    errors = []
    for cell in nb.cells:
        if 'outputs' in cell:
            for output in cell['outputs']:
                if output.output_type == 'error':
                    errors.append(output)

    return nb, errors


def test_py_notebook(py_p):
    with py_p.open("r") as f:
        nb = jupytext.read(f)

    print("#########################################################")
    print(str(py_p))
    nb, errors = run_nbnode(nb, run_path=py_p.parent)
    return str(py_p), errors


def is_notebook(py_p):
    with py_p.open("r") as f:
        text = f.read()
    pattern = "formats: ipynb,py:light"
    return (re.search(pattern, text) is not None)


def test_notebooks_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "target",
        type=str,
        help="""The name of a notebook file or
        a directory to search recursively for notebooks"""
    )
    parser.add_argument(
        "-a",
        "--avoid",
        type=str,
        help="""regular pattern to filter out notebooks or directories 
        to avoid, e.g. '.*deprecated/' """
    )
    args = parser.parse_args()
    # create a filter ff
    if args.avoid is not None:
        rex = re.compile(args.avoid)
        def ff(s):
            return (rex.match(s) is None) & is_notebook(Path(s))
    else:
        def ff(s):
            return is_notebook(Path(s))

    t_p = Path(args.target)
    if t_p.is_dir():
        print("directory")
        notebook_paths = [
            Path(s) for s in glob(f"{args.target}/**/*.py", recursive=True) 
            if ff(s)
        ]

    else:
        notebook_paths = [t_p]

    test_notebooks(notebook_paths)    


def test_notebooks(notebook_paths: List[Path]):

    print([str(p) for p in notebook_paths])
    #all_errs = all_errors(notebook_paths)
    def add_errors(acc, p):
        tup = test_py_notebook(p)
        s, errors = tup
        return acc + [tup] if len(errors) > 0 else acc

    all_errs = reduce(add_errors, notebook_paths, [])

    le = len(all_errs)
    if le > 0:
        print(f"{le} errors")
        print(all_errs)
        sys.exit(1)

