import os
import pandas as pd
from dapla_metadata.datasets import Datadoc

def convert_dat_populate_new_datadoc(flatfile: str,
                                     output_parquet: str,
                                     overwrite: bool = False) -> tuple[pd.DataFrame, Datadoc]:
    # Open data
    df = datadok_open_flatfile_from_path(flatfile)
    
    # Get old meta from old datadok
    meta_old = datadok_file_description_by_path(flatfile)
    
    # Write data
    if os.path.isfile(output_parquet) and not overwrite:
        raise IOError(f"File already exists: {output_parquet}")
    df.to_parquet(output_parquet)
    
    # Make new datadoc, metadata
    meta = Datadoc(dataset_path = output_parquet)
    return meta

    # Populate new datadoc model with stuff from old datadoc
    meta, codelists = migrate_meta_datadok_oldnew(meta_old, meta)
    
    # Save codelists to klass-xmls
    for var_name, code in codelists.items():
        codemeta = code["CodelistMeta"]
        codes = code["Codes"]
        
        # Add varname to outpath
        
        # Save klass-xml of the codelist
        
        # Where to save the metadata about the codelist?
        # "Vardok" .json?
    
    # Save changes to meta
    meta.write_metadata_document()
    
    return df, meta


def migrate_meta_datadok_oldnew(meta_old: OrderedDict[str, Any],
                                meta: Datadoc) -> Datadoc:
    
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
    