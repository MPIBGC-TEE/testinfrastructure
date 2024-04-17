#!/usr/bin/env python3
from string import Template
from pathlib import Path
import sys
import os
from collections import namedtuple
dir_path=Path(__file__).parent
file_name=Path(os.path.basename(__file__))
sys.path.insert(0,dir_path)
import shortesRelativePath as srp
from difflib import Differ

out_path=Path(".")
srp=srp.rp(s=out_path,t=dir_path)

t1=Template("""# This file has been automatically  procuded by ${fn}  

""")
t2a=Template("""# If we use conda or one of its derivatives we
# - install as many of the dependencies via conda 
# - block pip from installing them by the "--no-deps" flag
#  -and leave only the src packages for pip (for which there are no conda packages}.
# This leaves conda in control of your environment and avoides pip reinstalling 
# packages that are already installed by conda but not 
# detected by pip. This happens only for some packages (e.g. python-igraph) 
# but is a known problem and does affect us.
${command} install -y -c conda-forge --file requirements.test --file requirements.doc --file requirements.non_src --file requirements.conda_extra
""")
t2b="""# If we use conda or one of its derivatives we
# If you do not use conda but only pip, you do not have to preinstall i
# any requirements since pip will also find and install them from the setup.py 
# file directly.
"""
t3=Template(
"""# We install the dependencies that are not on pypy directly from github repos
# This is not possible with conda (therefore we use pip here)
# Do not do this (comment the following lines) 
# if you have checked out these repos and installed the code in developer mode 
${command} install --upgrade pip
${command} install ${flags} -r requirements.github

# The following line installs the package without checking out the repository directly from github
# if you want to install it in develop mode (after checking out the repo) comment this line and
# use "$command -e ." instead in the same directory where this file lives. 
${command} install ${flags} -r pkg.github
""")
txt1 = t1.substitute(
    fn=srp.joinpath(file_name)
)
pip_trunk="pip"

def write(command,suffix,txt):
    script_file_name=f"install_{command}.{suffix}"
    with Path(script_file_name).open("w") as f:
        f.write(txt)

def conda_like_txt(conda_command, pip_command):
    return txt1 + t2a.substitute(
        command=conda_command
    ) + t3.substitute(
        command=pip_command,
        flags="--no-deps"
    )

def pip_txt(pip_command):
    return txt1 + t2b + t3.substitute(
        command=pip_command,
        flags=""
    )
combi = namedtuple("combi",["suff","pref"])

for c in [
        combi("bat","call "),
        combi("sh", "")
    ]:
    write(
        command=pip_trunk,
        suffix=c.suff, 
        txt=pip_txt(f"{c.pref} {pip_trunk}")
    )
    for command in ["conda","mamba","micromamba"]:
        write(
            command=command,
            suffix=c.suff, 
            txt=conda_like_txt(
                conda_command=f"{c.pref} {command}", 
                pip_command=f"{c.pref} {pip_trunk}"
            )
        )
