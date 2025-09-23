import json
import os
from pathlib import Path

import pandas as pd

from ssb_tbmd_apis.operations.operations_datadok import datadok_file_description_by_path


def datadok_vars_dataframe_by_path(path: Path) -> pd.DataFrame:
    """Read datadok file and convert it to a pandas DataFrame.

    Args:
        path: Path to the datadok file.

    Returns:
        pd.DataFrame: DataFrame containing the datadok variables.
    """
    if os.environ.get("DAPLA_REGION", "") == "ON_PREM":
        gjfor_ddok = datadok_file_description_by_path(Path(path))
    else:
        with open(path) as migrerdok:
            gjfor_ddok = json.load(migrerdok)
    for_pandas_dict = {
        var["Title"]["_value_1"]: var["Properties"]
        for var in gjfor_ddok["ContextVariable"]
    }
    return pd.DataFrame(for_pandas_dict)
