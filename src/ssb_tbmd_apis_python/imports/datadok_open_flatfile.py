import os, glob

from ssb_tbmd_apis_python.imports.dtype_mapping import dtypes_datadok_to_pandas
from ssb_tbmd_apis_python.operations.operations_datadok import datadok_vars_dataframe_by_path

import pandas as pd


def datadok_open_flatfile_from_path(path: str, **read_fwf_params: Any) -> pd.DataFrame:
    if "encoding" not in read_fwf_params:
        read_fwf_params["encoding"] = "latin1"
    var_df = datadok_vars_dataframe_by_path(path)
    dtypes = dtypes_datadok_to_pandas(var_df)
    return pd.read_fwf(look_for_file(path),
                       dtypes=dtypes,
                       widths=var_df.T["Length"].to_list(),
                       names=dtypes.keys(),
                       na_values=".",
                       **read_fwf_params,
                      )

def look_for_file(path: str) -> str:
    # Attempt one, look for specific file
    if os.path.isfile(path):
        return path
    
    # Attempt two, look for common file extensions
    known_extensions = ["", ".dat", ".txt"]
    path_no_ext = path.rsplit(".", 1)[0]
    for ext in known_extensions:
        check_path = path_no_ext + ext
        if os.path.isfile(check_path):
            return check_path
    
    # Attempt three, look to see if we can find single match using glob
    glob_result = glob.glob(path_no_ext + "*")
    if len(glob_result) == 1:
        return glob_result[0]
    
    raise FileNotFoundError("Cant find single file with that path on local drive.")
    