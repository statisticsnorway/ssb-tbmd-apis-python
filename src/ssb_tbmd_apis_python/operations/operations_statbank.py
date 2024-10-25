"""
GetStatbankMetaByTabelId
Returnerer metadata fra tabell i statistikkbanken med gitt tabellid. F.eks 03886

GetStatbankMetaByTabelName
Returnerer metadata fra tabell i statistikkbanken med gitt tabellnavn. F.eks Raadyr

GetTableIdsByConceptVariableId
Returnerer vardokreferanse og tilhørende tabeller i statistikkbanken til gitt vardokid. F.eks 1756
"""

from collections import OrderedDict
from ssb_tbmd_apis_python.zeep_client import get_zeep_client
import zeep
import pandas as pd


def statbank_meta_by_table_id():
    pass

def statbank_meta_by_table_name():
    pass

def statbank_table_ids_by_concept_variable_id():
    pass