# This file has been automatically  procuded by scripts/make_installers.sh  
# If we use conda or one of its derivatives we
# - install as many of the dependencies via conda 
# - block pip from installing them by the "--no-deps" flag
#  -and leave only the src packages for pip (for which there are no conda packages}.
# This leaves conda in control of your environment and avoides pip reinstalling 
# packages that are already installed by conda but not 
# detected by pip. This happens only for some packages (e.g. python-igraph) 
# but is a known problem and does affect us.
 mamba install -y -c conda-forge --file requirements.test --file requirements.doc --file requirements.non_src --file requirements.conda_extra
# We install the dependencies that are not on pypy directly from github repos
# This is not possible with conda (therefore we use pip here)
# Do not do this (comment the following lines) 
# if you have checked out these repos and installed the code in developer mode 
 pip install --upgrade pip
 pip install --no-deps -r requirements.github

# The following line installs the package without checking out the repository directly from github
# if you want to install it in develop mode (after checking out the repo) comment this line and
# use " pip -e ." instead in the same directory where this file lives. 
 pip install --no-deps -r pkg.github