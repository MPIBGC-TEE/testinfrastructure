fn="requirements.conda"
mamba update mamba
mamba install -y python
python create_conda_requirement_list.py ${fn} 
mamba install  -y --file ${fn}
pip install -e .
