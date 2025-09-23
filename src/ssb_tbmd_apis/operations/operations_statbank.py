"""Operations supported by the Statbank TBMD API."""

from collections import OrderedDict
from typing import Any

from ssb_tbmd_apis.zeep_client import get_zeep_serialize


def statbank_meta_by_table_id(table_id: str | int) -> OrderedDict[str, Any]:
    """Returnerer metadata fra tabell i statistikkbanken med gitt tabellid. F.eks 03886.

    Args:
        table_id: The id of the table.

    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("statbank", "GetStatbankMetaByTabelId", table_id)


def statbank_meta_by_table_name(table_name: str) -> OrderedDict[str, Any]:
    """Returnerer metadata fra tabell i statistikkbanken med gitt tabellnavn. F.eks Raadyr.

    Args:
        table_name: The name of the table.

    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("statbank", "GetStatbankMetaByTabelName", table_name)


def statbank_table_ids_by_concept_variable_id(var_id: str) -> OrderedDict[str, Any]:
    """Returnerer vardokreferanse og tilhørende tabeller i statistikkbanken til gitt vardok-id. F.eks 1756.

    Args:
        var_id: The id of the concept variable.

    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("statbank", "GetTableIdsByConceptVariableId", var_id)
