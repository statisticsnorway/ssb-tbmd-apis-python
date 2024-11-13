import os, json
from ssb_tbmd_apis.operations.operations_datadok import datadok_file_description_by_path
import pandas as pd


def datadok_vars_dataframe_by_path(path: str) -> pd.DataFrame:
    if os.environ.get("DAPLA_REGION", "") == "ON_PREM":
        gjfor_ddok = datadok_file_description_by_path(path)
    else:
        with open(path, "r") as migrerdok:
            gjfor_ddok = json.load(migrerdok)
    for_pandas_dict = {var["Title"]["_value_1"]: var["Properties"] for var in gjfor_ddok["ContextVariable"]}
    return pd.DataFrame(for_pandas_dict)