def datadok_vars_dataframe_by_path(path: str) -> pd.DataFrame:
    gjfor_ddok = datadok_file_description_by_path(path)
    for_pandas_dict = {var["Title"]["_value_1"]: var["Properties"] for var in gjfor_ddok["ContextVariable"]}
    return pd.DataFrame(for_pandas_dict)