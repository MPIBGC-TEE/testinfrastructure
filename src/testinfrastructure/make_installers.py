#!/usr/bin/env python3
from typing import List,Tuple
from string import Template
from pathlib import Path
import os
from collections import namedtuple
dir_path=Path(__file__).parent
#file_name=Path(os.path.basename(__file__))
from testinfrastructure import shortesRelativePath as srp
import inspect
from functools import reduce
#out_path=Path(".")
#srp=srp.rp(s=out_path,t=dir_path)
#
t1 = Template("""# This file has been automatically procuded by the function: 
# ${func_name} and those of the following files 
# that are present in the root folder of the repo: 
# requirements.non_src, 
# requierements.conda_extra, 
# requirements.test, 
# requirements.doc, 
# requirements.github, 
# pkg.github 
#
# If you have testinfrastructure installed
# you can change the requirement files and recreate all the install 
# scripts automatically by running the command: 
# $$make_installers 
""")

t_pip_update = Template(
"""
${command} install --update pip
""")

t_github=Template(
"""
# We install the dependencies that are not on pypy directly from github repos
# This is not possible with conda (therefore we use pip here)
# Do not do this (comment the following lines) 
# if you have checked out these repos and installed the code in developer mode
${command} install ${flags} ${reqs_github}
""")


t_conda_pkgs=Template("""
# If we use conda or one of its derivatives we
# - install as many of the dependencies via conda 
# - block pip from installing them by the "--no-deps" flag
#  -and leave only the src packages for pip (for which there are no conda packages}.
# This leaves conda in control of your environment and avoides pip
# reinstalling packages that are already installed by conda but not
# detected by pip. 
# This happens only for some packages (e.g.  # python-igraph) 
# but is a known problem at the time of writing and does affect us.
${command} install ${flags} ${reqs}
""")

t_test=Template("""
# To run the tests (which is recommended but not necessary for the package to work) 
# you need some extra packages which can be installed by uncommenting the following line:
${command} install ${flags} ${reqs}
""")

t_doc=Template("""
# If you want to develop the package including the documentation you need some extra tools which can be installed by uncommenting the following line:
# ${command} install ${flags} ${reqs}
""")



t_pip_pkg=Template(
"""
# The following line installs the package without checking out the repository directly from github
${command} install ${flags} ${pkg}

# if you want to install it in develop mode (after checking out the repo) comment the previous line and
# execute the following line instead, in the same directory where this file lives. 
# ${command} install ${flags} -e .
""")


def add_pkgs(pkgs,fn):
    pn=Path(fn)
    if pn.exists():
        with pn.open("r") as f:
            flns=f.readlines()
        fpkgs=[l.strip() for l in flns]
    else:
        fpkgs = []
    return pkgs + fpkgs

def pkg_str(requirement_file_names:List) -> str:
    return " ".join(
        reduce(
            add_pkgs,
            requirement_file_names,
            []
        )
    )


def write(command,suffix,txt):
    script_file_name=f"install_{command}.{suffix}"
    with Path(script_file_name).open("w") as f:
        f.write(txt)

def conda_like_txt(preamble, conda_command, pip_command):
    def add_txt_2(txt,tupel):
        temp, fns = tupel
        pkgs = pkg_str(fns)
        res=txt if len(pkgs) == 0 else txt+"\n"+temp.substitute(
            command=conda_command,
            flags="-y -c conda-forge",
            reqs=pkgs
        )
        return res

    tuples_2=[
        (t_conda_pkgs,["requirements.non_src", "requirements.conda_extra"]),
        (t_test,["requirements.test"]),
        (t_doc,["requirements.doc"]),
    ]
    txt2=reduce(
        add_txt_2,
        tuples_2,
        ""
    )
        
    def add_txt_3(txt,tupel):
        temp, fns = tupel
        pkgs = pkg_str(fns)
        res=txt if len(pkgs) == 0 else txt+"\n"+temp.substitute(
            command=pip_command,
            flags="--no-deps",
            reqs=pkgs
        )
        return res

    tuples_3=[
        (t_github,["requirements.github"]),
    ]
    txt3=reduce(
        add_txt_3,
        tuples_3,
        ""
    )

    txt4=t_pip_pkg.substitute(
        command=pip_command,
        flags="--no-deps",
        pkg=pkg_str(["pkg.github"])
        ) 
    return (
        preamble + txt2 + txt3 + txt4 #+
    )

def pip_txt(
        preamble: str, 
        pip_command: str
    )-> str:

    def add_txt_3b(txt,tupel):
        temp, fns = tupel
        pkgs = pkg_str(fns)
        res=txt if len(pkgs) == 0 else txt+"\n"+temp.substitute(
            command=pip_command,
            flags="",
            reqs=pkgs
        )
        return res

    tuples_3b=[
        (t_github,["requirements.github"]),
        (t_test,["requirements.test"]),
        (t_doc,["requirements.doc"]),
    ]
    txt3=reduce(
        add_txt_3b,
        tuples_3b,
        ""
    )
    txt4=t_pip_pkg.substitute(
        command=pip_command,
        flags="",
        pkg=pkg_str(["pkg.github"])
        ) 
    #from IPython import embed;embed()
    return (
		preamble 
        + t_pip_update.substitute(command=pip_command) 
        + txt3
        + txt4
	)

def make_installers_cmd():    
    pip_trunk="pip"
    func=inspect.currentframe().f_code
    mod=inspect.getmodule(func)
    fn=f"{mod.__name__}.{func.co_name}"
    preamble=t1.substitute(func_name=fn)
    combi = namedtuple("combi",["suff","pref"])
    
    for c in [
    	    # for windows we create a *.bat file and precede the command with "call"  
            combi("bat","call "), 
    	    # for linux we create a *.sh file and do not need to precede the command 
            combi("sh", "")
        ]:
        write(
            command=pip_trunk,
            suffix=c.suff, 
            txt=pip_txt(
                preamble=preamble,
                pip_command=f"{c.pref} {pip_trunk}"
            )
        )
        for command in ["conda","mamba","micromamba"]:
            write(
                command=command,
                suffix=c.suff, 
                txt=conda_like_txt(
                    preamble=preamble,
                    conda_command=f"{c.pref} {command}", 
                    pip_command=f"{c.pref} {pip_trunk}"
                )
            )
