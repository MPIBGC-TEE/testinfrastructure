# This file has been automatically  procuded by scripts/make_installers.sh  
# If we use conda or one of its derivatives we
# If you do not use conda but only pip, you do not have to preinstall i
# any requirements since pip will also find and install them from the setup.py 
# file directly.
# so we only install stuff explicitly that is not a dependency of the package
# but necessary for testing.
call  pip -r requirements.test
# We install the dependencies that are not on pypy directly from github repos
# This is not possible with conda (therefore we use pip here)
# Do not do this (comment the following lines) 
# if you have checked out these repos and installed the code in developer mode 
call  pip install --upgrade pip
call  pip install  -r requirements.github

# The following line installs the package without checking out the repository directly from github
# if you want to install it in develop mode (after checking out the repo) comment this line and
# use "call  pip -e ." instead in the same directory where this file lives. 
call  pip install  -r pkg.github
