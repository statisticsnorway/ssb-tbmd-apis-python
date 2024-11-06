import os, json
from pathlib import Path
import pandas as pd
from dapla_metadata.datasets import Datadoc
from dapla_metadata.datasets.statistic_subject_mapping import StatisticSubjectMapping
from ssb_tbmd_apis.tbmd_logger import logger
from ssb_tbmd_apis.imports.datadok_open_flatfile import datadok_open_flatfile_from_path
from ssb_tbmd_apis.operations.operations_datadok import datadok_file_description_by_path
from ssb_tbmd_apis.paths.try_variations import swap_dollar_sign

from collections import OrderedDict
from typing import Any


def save_migrerdok_for_flatfile(flatfile: str | Path,
                                overwrite: bool = False) -> Path:   
    ddok_contents, ddok_save_path = datadok_file_description_by_path(flatfile)
    
    # Get old meta from old datadok
    ddok_path = ddok_save_path.parent / (ddok_save_path.stem + "__MIGRERDOK.json")
    ddok_path = swap_dollar_sign(ddok_path)
    if not ddok_path.is_file() or overwrite:
        ddok_path.parent.mkdir(parents=True, exist_ok=True)
        with open(ddok_path, "w") as ddok_file:
            json.dump(ddok_contents, ddok_file, default=str)
        logger.info(f"Wrote datadok contents to {ddok_path}")
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
    