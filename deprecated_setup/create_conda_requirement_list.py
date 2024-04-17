from pathlib import Path
from functools import reduce
import re
import distutils.core
import sys

def extra_req_list_from_path_str(ps):
    if ps.exists():
        with Path(ps).open("r") as f:
            lines=f.readlines()
    else:
        lines = []

    return list(
        map(
            lambda line: line.strip(),
            filter(
                lambda line: re.compile("^\w").match(line),
                lines 
            )
        )
    )


def setup_req_list_from_path_str(ps):
    setup = distutils.core.run_setup(ps)
    return setup.install_requires


res = (
    [
        f"# automatically created by  {sys.argv[0]}",
        "# from setup.py and requirements.conda.extra"
    ]    
    +
    extra_req_list_from_path_str(Path("requirements.conda.extra"))
    +
    setup_req_list_from_path_str(Path("setup.py"))
)

with Path(sys.argv[1]).open("w") as f:
    f.write("\n".join(res))
