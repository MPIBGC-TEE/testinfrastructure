set fn ="requirements.conda"
call conda update -y -n base -c defaults conda
call conda install -y python
call python create_conda_requirement_list.py %fn%
call conda install -y --file %fn%
call pip install -e . 
