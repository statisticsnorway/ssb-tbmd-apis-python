from collections import OrderedDict
from ssb_tbmd_apis_python.zeep_client import get_zeep_client
import zeep
import pandas as pd



def datadok_file_description_by_path(path: str) -> OrderedDict:
    client = get_zeep_client()
    response = client.service.GetFileDescriptionByPath(path)
    return zeep.helpers.serialize_object(response)


def datadok_vars_dataframe_by_path(path: str) -> pd.DataFrame:
    gjfor_ddok = datadok_file_description_by_path(path)
    for_pandas_dict = {var["Title"]["_value_1"]: var["Properties"] for var in gjfor_ddok["ContextVariable"]}
    return pd.DataFrame(for_pandas_dict)
