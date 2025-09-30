import os
from pathlib import Path
from typing import Any

import pandas as pd

from ssb_tbmd_apis.imports.datadok_meta import datadok_vars_dataframe_by_path
from ssb_tbmd_apis.imports.dtype_mapping import dtypes_datadok_to_pandas
from ssb_tbmd_apis.paths.try_variations import look_for_file_on_disk


def datadok_open_flatfile_from_path(
    path: Path, ddok_path: Path | None = None, **read_fwf_params: Any
) -> pd.DataFrame:
    """Open a flat file from Datadok and convert it to a pandas DataFrame.

    Args:
        path: Path to the flat file.
        ddok_path: Path to the Datadok file (optional).
        read_fwf_params: Additional parameters for reading the flat file.

    Returns:
        pd.DataFrame: DataFrame containing the data from the flat file.
    """
    if "encoding" not in read_fwf_params:
        read_fwf_params["encoding"] = "latin1"

    if ddok_path is not None:
        var_df = datadok_vars_dataframe_by_path(Path(ddok_path))
    else:
        var_df = datadok_vars_dataframe_by_path(Path(path))

    dtypes = dtypes_datadok_to_pandas(var_df)

    floats = [k for k, v in dtypes.items() if "float" in v.lower()]

    for fl in floats:
        dtypes[fl] = "string"

    if "ON_PREM" == os.environ.get("DAPLA_REGION", ""):
        path = look_for_file_on_disk(path)
    df: pd.DataFrame = pd.read_fwf(
        path,
        widths=var_df.T["Length"].to_list(),
        names=dtypes.keys(),
        na_values=".",
        converters=dict.fromkeys(dtypes, str) ** read_fwf_params,
    ).astype(dtypes)
    # Handle floats to convert
    for col in floats:
        df[col] = df[col].str.replace(",", ".").astype("Float64")

    df.columns = [x.lower() for x in df.columns]
    return df
