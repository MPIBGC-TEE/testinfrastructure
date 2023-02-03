fn="requirements.conda"
conda update -y -n base -c defaults conda
conda install -y python
python create_conda_requirement_list.py ${fn} 
conda install -c conda-forge -y --file ${fn}
pip install -e .
