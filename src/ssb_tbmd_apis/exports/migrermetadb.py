import json
from collections import OrderedDict
from pathlib import Path
from typing import Any

import zeep

from ssb_tbmd_apis.operations.operations_metadb import metadb_codelist_by_id
from ssb_tbmd_apis.operations.operations_metadb import metadb_codelists
from ssb_tbmd_apis.paths.try_variations import swap_dollar_sign
from ssb_tbmd_apis.tbmd_logger import logger


def get_metadb_vars(varnames: list[str]) -> dict[str, OrderedDict[str, Any]]:
    """Get metadb variables from the API based on the provided variable names.

    Args:
        varnames: List of variable names to search for in the metadb.

    Returns:
        dict: A dictionary where the keys are the variable names and the values are
              the corresponding metadb codelists.
    """
    metadb = {
        x["CodelistMeta"]["Title"]["_value_1"]: x["id"] for x in metadb_codelists()
    }
    codelist_codes = {}
    for var in varnames:
        for meta_col, meta_id in metadb.items():
            if meta_col.lower().endswith(var.lower()):
                logger.info(f"Found: {var} at end of {meta_col} with id {meta_id}")
                try:
                    codelist_codes[meta_col] = metadb_codelist_by_id(meta_id)
                except zeep.exceptions.Fault as e:
                    logger.warning(
                        f"Couldnt get {meta_col} - {meta_id} from the API: {e}"
                    )
                break
    return codelist_codes


def save_metadb_vars(
    varnames: list[str], outpath: Path, overwrite: bool = False
) -> dict[str, OrderedDict[str, Any]]:
    """Save metadb variables to a JSON file.

    Args:
        varnames: List of variable names to save.
        outpath: Path to the output JSON file.
        overwrite: Whether to overwrite the file if it exists.

    Returns:
        dict: A dictionary where the keys are the variable names and the values are
              the corresponding metadb codelists.

    Raises:
        OSError: If file already exists, and overwrite is not set to True.
    """
    outpath = swap_dollar_sign(Path(outpath))
    logger.info(f"After swapping dollar {outpath}")
    suffix = "__MIGRERMETADB.json"
    if not outpath.name.endswith(suffix):
        outpath = outpath.parent / (outpath.stem + suffix)

    codelists = get_metadb_vars(varnames)
    if not outpath.is_file() or overwrite:
        with open(outpath, "w") as metadbfile:
            json.dump(codelists, metadbfile, default=str)
        logger.info(f"Wrote migrer metadb file to: {outpath}")
    else:
        raise OSError(
            f"File already exists, set overwrite to True if you want to overwrite: {outpath}."
        )
    return codelists
