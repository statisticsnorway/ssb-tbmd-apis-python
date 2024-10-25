"""
GetCodelistById
Rutinen skal returnere én kodeliste med alle attributter basert på gitt Id eller urn. F.eks 228589 urn:ssb:codelist:datadok:228589

GetCodelistByReference
Rutinen skal returnere én kodeliste med alle attributter basert på gitt Datadokreferanse for en filvariabel. F.eks $FOB/person/arkiv/personfil/g2001/spes_reg_type

GetCodelists
Returnerer en oversikt over hvilke kodelister som finnes i Datadok.

GetContextVariableById
Rutinen skal returnere én filvariabel med alle attributter (navn, beskrivelse, datatype, lengde, startposisjon, antall desimaler, verdiområde, kommentar, kodeliste) basert på gitt variabel Id eller urn. F.eks 865507 eller urn:ssb:contextvariable:datadok:865507

GetContextVariableByReference
Rutinen skal returnere én filvariabel med alle attributter (navn, beskrivelse, datatype, lengde, startposisjon, antall desimaler, verdiområde, kommentar, kodeliste) basert på gitt datadokreferanse. F.eks. $FOB/person/arkiv/personfil/g2001/spes_reg_type

GetFileDescriptionById
Rutinen skal returnere én filbeskrivelse basert på gitt filbeskrivelse Id eller urn. F.eks 1288400 eller urn:ssb:dataset:datadok:1288400

GetFileDescriptionByPath
Rutinen skal returnere én filbeskrivelse basert på gitt Datadok sti. F.eks. FOB/person/arkiv/personfil/g2001
"""


from collections import OrderedDict
from ssb_tbmd_apis_python.zeep_client import get_zeep_client
from ssb_tbmd_apis_python.prodsone.linux_stammer import linux_stammer
from ssb_tbmd_apis_python.tbmd_logger import logger

import zeep
from zeep.exceptions import Fault
import pandas as pd






def datadok_file_description_by_path(path: str) -> OrderedDict:
    client = get_zeep_client()        
    response = _try_path_possibilities(path, client)
    return zeep.helpers.serialize_object(response)

def _try_path_possibilities(path: str, client) -> requests.Response:
    for try_path in _make_path_possibilites(path):
        try:
            response = client.service.GetFileDescriptionByPath(try_path)
        except Fault as e:
            logger.info(f"Found no response in the API for path {try_path}")
    raise FileNotFoundError("Could not find the path you specified in the Datadok-api.")

    
def _make_path_possibilites(path: str) -> list[str]:
    
    
def datadok_vars_dataframe_by_path(path: str) -> pd.DataFrame:
    gjfor_ddok = datadok_file_description_by_path(path)
    for_pandas_dict = {var["Title"]["_value_1"]: var["Properties"] for var in gjfor_ddok["ContextVariable"]}
    return pd.DataFrame(for_pandas_dict)