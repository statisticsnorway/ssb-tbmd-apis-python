import os, json
from pathlib import Path
import pandas as pd
from dapla_metadata.datasets import Datadoc
from dapla_metadata.datasets.statistic_subject_mapping import StatisticSubjectMapping
from ssb_tbmd_apis.tbmd_logger import logger
from ssb_tbmd_apis.imports.datadok_open_flatfile import datadok_open_flatfile_from_path
from ssb_tbmd_apis.operations.operations_datadok import datadok_file_description_by_path
from ssb_tbmd_apis.paths.try_variations import swap_dollar_sign
from fagfunksjoner.paths.versions import next_version_path, latest_version_path

from collections import OrderedDict
from typing import Any


def save_migrerdok_for_flatfile(flatfile: str | Path,
                                version_up: bool = True,
                                overwrite: bool = False) -> Path:   
    # Get old meta from old datadok
    ddok_contents, ddok_save_path = datadok_file_description_by_path(flatfile)
    
    # Construct path
    ddok_path = ddok_save_path.parent / (ddok_save_path.stem + "__MIGRERDOK_v1.json")
    ddok_path = swap_dollar_sign(ddok_path)
    
    # Write non-existing file / overwrite
    if not ddok_path.is_file() or overwrite:
        ddok_path.parent.mkdir(parents=True, exist_ok=True)
        with open(ddok_path, "w") as ddok_file:
            json.dump(ddok_contents, ddok_file, default=str)
        logger.info(f"Wrote datadok contents to {ddok_path}")
    # File exists, and we want to version up
    elif version_up:
        # Get highest available version path on disk
        path_highest_version = latest_version_path(str(ddok_path))
        
        # Check if content is the same
        with open(path_highest_version) as old_json:        
            json_old = json.load(old_json)
        equal = deep_equal(json.dumps(json_old, default=str), json.dumps(ddok_contents, default=str))
        
        # If different, bump highest available path, and write to empty path
        if not equal:
            bump_path = next_version_path(path_highest_version)
            with open(bump_path, "w") as ddok_file:
                logger.info(f"Versioning up path, since we found existing file: {bump_path}")
                json.dump(ddok_contents, ddok_file, default=str)
        else:
            logger.info("Datadok contents equals old version, no point in versioning it up.")
    else:
        raise OSError(f"Not overwriting existing file {ddok_path}")  
    return ddok_path

def get_colnames_from_migrerdok(migrerdok: str | Path) -> list[str]:
    path = swap_dollar_sign(migrerdok)
    with open(path, "r") as migrerout:
        contents = json.load(migrerout)
    colnames = [x["Title"]["_value_1"] for x in contents["ContextVariable"]]
    return colnames

        
def convert_dat_save_migrerdok(flatfile: str,
                                output_parquet: str,
                                overwrite: bool = False) -> tuple[pd.DataFrame, Datadoc]:
    raise NotImplementedError()
    
    df = datadok_open_flatfile_from_path(flatfile)
    
    
    meta_old = save_migrerdata_for_flatfile(flatfile, overwrite)
    
    meta_doc = Datadoc(output_parquet,
        statistic_subject_mapping=StatisticSubjectMapping(source_url=None)
           )
    meta_doc = migrate_meta_datadok_oldnew(meta_old, meta_doc)
    
    return df, meta_doc

def migrate_meta_datadok_oldnew(meta_old: str | Path,
                                meta: str | Path) -> Datadoc:
    raise NotImplementedError()
    
    # Title
    title = meta_old["Title"]["_value_1"]
    
    # Description
    desc = meta_old["Description"]["_value_1"]
    
    # ContactInformation
    person = meta_old["ContactInformation"]["Person"]
    division = meta_old["ContactInformation"]["Division"]
    
    # ContextVariable
    variables = meta_old["ContextVariable"]
    
    codelists = {}
    for var in variables:
        var_title = var["Title"]["_value_1"]
        var_desc = var["Description"]["_value_1"]
        var_comment = var["Comments"]
        var_ref = var["VariableReference"]
        
        if var["Codelist"] is not None:
            codelists[var_title] = var["Codelist"]
        
        
    return meta, codelists
    
    
def deep_equal(dict1, dict2):
    """
    Recursively check equality between two dictionaries, ignoring the order of lists.

    Args:
        dict1 (dict): The first dictionary to compare.
        dict2 (dict): The second dictionary to compare.

    Returns:
        bool: True if the dictionaries are equal, otherwise False.
    """
    if type(dict1) != type(dict2):
        return False

    if isinstance(dict1, dict):
        if dict1.keys() != dict2.keys():
            return False
        return all(deep_equal(dict1[key], dict2[key]) for key in dict1)

    if isinstance(dict1, list):
        if len(dict1) != len(dict2):
            return False
        return sorted(deep_equal(item, dict2[i]) if isinstance(item, dict) else item for i, item in enumerate(dict1))
        
    return dict1 == dict2