import os, glob
from typing import Any

from ssb_tbmd_apis.tbmd_logger import logger
from ssb_tbmd_apis.imports.dtype_mapping import dtypes_datadok_to_pandas
from ssb_tbmd_apis.imports.datadok_meta import datadok_vars_dataframe_by_path
from ssb_tbmd_apis.paths.try_variations import look_for_file_on_disk

import pandas as pd




def datadok_open_flatfile_from_path(path: str, ddok_path: str | None = None, **read_fwf_params: Any) -> pd.DataFrame:
    if "encoding" not in read_fwf_params:
        read_fwf_params["encoding"] = "latin1"
        
    if ddok_path is not None:
        var_df = datadok_vars_dataframe_by_path(ddok_path)
    else:
        var_df = datadok_vars_dataframe_by_path(path)
        
    dtypes = dtypes_datadok_to_pandas(var_df)
    df = pd.read_fwf(look_for_file_on_disk(path),
                       widths=var_df.T["Length"].to_list(),
                       names=dtypes.keys(),
                       na_values=".",
                       converters={k: str for k in dtypes.keys()},
                       **read_fwf_params,
                      ).astype(dtypes)
    df.columns = [x.lower() for x in df.columns]
    return df

    