#!/usr/bin/env python3
from string import Template
from pathlib import Path
import os
from collections import namedtuple
dir_path=Path(__file__).parent
file_name=Path(os.path.basename(__file__))
from testinfrastructure import shortesRelativePath as srp
import inspect

#out_path=Path(".")
#srp=srp.rp(s=out_path,t=dir_path)
#
t1 = Template("""# This file has been automatically procuded by the function: 
# ${fn}  
""")
#txt1=t1.substitute( fn=srp.joinpath(file_name))
t2a=Template("""
# If we use conda or one of its derivatives we
# - install as many of the dependencies via conda 
# - block pip from installing them by the "--no-deps" flag
#  -and leave only the src packages for pip (for which there are no conda packages}.
# This leaves conda in control of your environment and avoides pip
# reinstalling packages that are already installed by conda but not
# detected by pip. 
# This happens only for some packages (e.g.  # python-igraph) 
# but is a known problem at the time of writing and does affect us.
${command} install -y -c conda-forge --file requirements.test  --file requirements.non_src --file requirements.conda_extra
# If you want to develop the package including the documentation you need some extra tools which can be installed by uncommenting the following line:
# ${command} install -y -c conda-forge --file requirements.doc 
""")
t2b=Template(
""" # If you do not use conda but only pip, you do not have to
preinstall 
# any requirements since pip will also find and install them from the
# setup.py file directly.  So we only install stuff explicitly that
# is not a dependency of the package but necessary for testing.
${command} install -r requirements.test
""")

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
pip_trunk="pip"

def write(command,suffix,txt):
    script_file_name=f"install_{command}.{suffix}"
    with Path(script_file_name).open("w") as f:
        f.write(txt)

def conda_like_txt(preamble, conda_command, pip_command):
    return preamble + t2a.substitute(
        command=conda_command
    ) + t3.substitute(
        command=pip_command,
        flags="--no-deps"
    )

def pip_txt(preamble, pip_command):
	return (
		preamble
		+ 
		t3.substitute(
        		command=pip_command,
        		flags=""
    		)
		+
		t2b.substitute(command=pip_command)
	)

def make_installers_cmd():    
    print(inspect.currentframe().f_code.co_name)
    f=inspect.currentframe().f_code
    mod=inspect.getmodule(f)
    preamble=t1.substitute(fn=f"{mod.__name__}.{f.co_name}")
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
            txt=pip_txt(preamble,f"{c.pref} {pip_trunk}")
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
