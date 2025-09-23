import pandas as pd


def dtypes_datadok_to_pandas(ddok_var_df: pd.DataFrame) -> dict[str, str]:
    """Map Datadok variable types to pandas dtypes.

    Args:
        ddok_var_df: DataFrame containing Datadok variable information.

    Returns:
        dict[str, str]: Dictionary mapping variable names to pandas dtypes.

    Raises:
        NotImplementedError: If an unsupported datatype is encountered.
    """
    if "Datatype" in ddok_var_df:
        df = ddok_var_df
    else:
        df = ddok_var_df.T
    dtypes: dict[str, str] = {}

    colname: str
    properties: dict[str, str]

    for colname, properties in df.iterrows():
        if "Tekst" == properties["Datatype"]:
            dtypes[colname] = "string[pyarrow]"
        elif properties["Datatype"] in ["Desimaltall", "Desim. (K)", "Desim. (P)"]:
            dtypes[colname] = "Float64"
        elif "Heltall" == properties["Datatype"]:
            dtypes[colname] = intwidth_to_pandas_dtype(properties["Length"])
        ## MISSING LOGIC FOR OTHER TYPES - DATES?
        else:
            raise NotImplementedError(
                f"Please program for more dtypes, like datetimes? {properties['Datatype']}"
            )

    return dtypes


def intwidth_to_pandas_dtype(precision: int) -> str:
    """Convert integer width to pandas dtype.

    Args:
        precision: Integer width.

    Returns:
        str: Corresponding pandas dtype.

    Raises:
        ValueError: If precision is too large for pandas Int types.
    """
    precision = int(precision)

    precisions = {
        3: "Int8",  # Fits in Int8 (-128 to 127)
        5: "Int16",  # Fits in Int16 (-32,768 to 32,767)
        10: "Int32",  # Fits in Int32 (-2,147,483,648 to 2,147,483,647)
        19: "Int64",  # Fits in Int64 (-9,223,372,036,854,775,808 to 9,223,372,036,854,775,807)
    }

    for pres_setting, dtype in precisions.items():
        if precision < pres_setting:
            return dtype
    raise ValueError(f"Precision {precision} is too large for pandas Int types")
