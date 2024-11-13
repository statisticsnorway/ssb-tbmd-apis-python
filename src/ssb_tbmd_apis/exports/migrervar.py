import json
from pathlib import Path
from typing import Any
from collections import OrderedDict

from ssb_tbmd_apis.operations.operations_vardok import vardok_concept_variables_by_owner
from ssb_tbmd_apis.paths.try_variations import swap_dollar_sign

def save_vardok_variables_belong_section(section: int,
                                         path: str | Path,
                                         overwrite: bool = False) -> OrderedDict[str, Any]:
    outpath = swap_dollar_sign(path)
    content = vardok_concept_variables_by_owner(section)
    if not outpath.is_file() or overwrite:
        with open(outpath, "w") as jsonfile:
            json.dump(content, jsonfile, default=str)
    else:
        raise OSError(f"Set overwrite to True, if you want to overwrtie: {outpath}")
    return content
    