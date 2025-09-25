import pandas as pd
import pytest

from ssb_tbmd_apis.imports.dtype_mapping import dtypes_datadok_to_pandas
from ssb_tbmd_apis.imports.dtype_mapping import intwidth_to_pandas_dtype


def test_text_mapping():
    df = pd.DataFrame({"Datatype": ["Tekst"], "Length": ["10"]}, index=["mycol"])
    result = dtypes_datadok_to_pandas(df)
    assert result == {"mycol": "string[pyarrow]"}


@pytest.mark.parametrize("dtype", ["Desimaltall", "Desim. (K)", "Desim. (P)"])
def test_decimal_mapping(dtype: str):
    df = pd.DataFrame({"Datatype": [dtype], "Length": ["10"]}, index=["col1"])
    result = dtypes_datadok_to_pandas(df)
    assert result == {"col1": "Float64"}


def test_integer_mapping_int32():
    df = pd.DataFrame({"Datatype": ["Heltall"], "Length": ["9"]}, index=["intcol"])
    result = dtypes_datadok_to_pandas(df)
    # 9 < 10, so Int32
    assert result == {"intcol": "Int32"}


def test_unknown_type_raises():
    df = pd.DataFrame({"Datatype": ["Ukjent"], "Length": ["10"]}, index=["x"])
    with pytest.raises(NotImplementedError):
        dtypes_datadok_to_pandas(df)


@pytest.mark.parametrize(
    "precision, expected",
    [
        (1, "Int8"),
        (4, "Int16"),
        (9, "Int32"),
        (18, "Int64"),
    ],
)
def test_intwidth_to_pandas_dtype_valid(precision, expected):
    assert intwidth_to_pandas_dtype(precision) == expected


def test_intwidth_too_large():
    with pytest.raises(ValueError):
        intwidth_to_pandas_dtype(25)
