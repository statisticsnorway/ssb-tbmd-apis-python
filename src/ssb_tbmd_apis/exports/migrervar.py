import json
from collections import OrderedDict
from pathlib import Path
from typing import Any

from ssb_tbmd_apis.operations.operations_vardok import vardok_concept_variables_by_owner
from ssb_tbmd_apis.paths.try_variations import swap_dollar_sign


def save_vardok_variables_belong_section(
    section: int, path: str | Path, overwrite: bool = False
) -> OrderedDict[str, Any]:
    """Save Vardok variables belonging to a section to a JSON file.

    Args:
        section: The section number to filter variables by.
        path: Path to the output JSON file.
        overwrite: Whether to overwrite the file if it exists.

    Returns:
        OrderedDict: A dictionary containing the variables belonging to the specified section.

    Raises:
        OSError: If the file already exists and overwrite is set to False.
    """
    outpath = swap_dollar_sign(path)
    content = vardok_concept_variables_by_owner(section)
    if not outpath.is_file() or overwrite:
        with open(outpath, "w") as jsonfile:
            json.dump(content, jsonfile, default=str)
    else:
        raise OSError(f"Set overwrite to True, if you want to overwrtie: {outpath}")
    return content
