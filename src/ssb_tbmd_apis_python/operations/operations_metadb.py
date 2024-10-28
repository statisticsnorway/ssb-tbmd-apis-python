"""Operations supported by the MetaDB TBMD API."""


from typing import Any
from collections import OrderedDict
from ssb_tbmd_apis_python.zeep_client import get_zeep_serialize


def metadb_codelist_by_id(codelist_id: int | str) -> OrderedDict[str, Any]:
    """Rutinen skal returnere én kodeliste basert på gitt kodeliste Id eller urn.
    
    F.eks 10013 eller urn:ssb:codelist:metadb:10013
    
    Args:
        codelist_id: Id for the codelist.
        
    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("metadb", "GetCodelistById", codelist_id)

def metadb_codelists() -> OrderedDict[str, Any]:
    """Rutinen skal returnere en oversikt over hvilke kodelister som finnes i metadb.
        
    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("metadb", "GetCodelists")

def metadb_context_variable_by_id(var_id: int | str) -> OrderedDict[str, Any]:
    """Rutinen skal returnere én variabel med alle attributter.
    
    Navn, fullt navn, datatype, lengde, desimaler, variabeltype, gyldig fra/til, datoformat, datering, endring, kodeliste og vardokreferanse.
    Basert på gitt variabel Id eller urn. Variablene må være godkjent for Internett. 
    
    F.eks 14739 eller urn:ssb:contextvariable:metadb:14739
    
    Args:
        var_id: Id for the codelist.
        
    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("metadb", "GetContextVariableById", var_id)


def metadb_description_by_id(table_id: int | str) -> OrderedDict[str, Any]:
    """Rutinen skal returnere én tabell med alle attributter.
    
    Overtema, subtema, navn, beskrivelse, gyldig fra/til og alle variabler basert på gitt tabell Id eller urn. 
    
    Tabellen og variablene må være godkjent for Internett. F.eks tabell id 11518 eller urn:ssb:dataset:metadb:11518
    
    Args:
        table_id: Id for the table.
        
    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("metadb", "GetDataDescriptionById", table_id)
    

def metadb_event_history_structure_by_id(project_id: int | str) -> OrderedDict[str, Any]:
    """Rutinen skal returnere ett prosjekt med tilhørende overtema, subtema, tabeller og variabler basert på gitt prosjekt Id eller urn.
    
    Gyldige prosjekt Id'er er 1001 og 1004. Gyldige urn'er er urn:ssb:project:metadb:1001 og urn:ssb:project:metadb:1004
    
    Args:
        project_id: Id for the project.
        
    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("metadb", "GetEventHistoryStructureById", project_id)
    