"""Operations supported by the Datadok TBMD API."""
import os
from typing import Any
from collections import OrderedDict
from ssb_tbmd_apis.zeep_client import get_zeep_serialize
from ssb_tbmd_apis.paths.try_variations import try_zeep_serialize_path

import zeep

def datadok_codelist_by_id(codelist_id: int | str) -> OrderedDict[str, Any]:
    """Rutinen skal returnere én kodeliste med alle attributter basert på gitt Id eller urn. 
    
    F.eks 228589 urn:ssb:codelist:datadok:228589.
    
    Args:
        codelist_id: Id for the codelist.
        
    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("datadok", "GetCodelistById", codelist_id)

def datadok_codelist_by_reference(codelist_ref: str) -> OrderedDict[str, Any]:
    """Rutinen skal returnere én kodeliste med alle attributter basert på gitt Datadokreferanse for en filvariabel. 
    
    F.eks $FOB/person/arkiv/personfil/g2001/spes_reg_type
    
    Args:
        codelist_ref: The path to check for datadok-files, usually using the dollar-stamme, and without file-extension.
        
    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("datadok", "GetCodelistByReference", codelist_ref)

def datadok_codelists() -> OrderedDict[str, Any]:
    """Returnerer en oversikt over hvilke kodelister som finnes i Datadok.
        
    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("datadok", "GetCodelists")


def datadok_context_variable_by_id(var_id: int | str) -> OrderedDict[str, Any]:
    """Rutinen skal returnere én filvariabel med alle attributter.
    
    navn, beskrivelse, datatype, lengde, startposisjon, antall desimaler, verdiområde, kommentar,
    kodeliste basert på gitt variabel Id eller urn. 
    F.eks 865507 eller urn:ssb:contextvariable:datadok:865507
    
    Args:
        var_id: The ID of the context variable.
        
    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("datadok", "GetContextVariableById", var_id)

def datadok_context_variable_by_reference(var_ref: str) -> OrderedDict[str, Any]:
    """Rutinen skal returnere én filvariabel med alle attributter.
    
    navn, beskrivelse, datatype, lengde, startposisjon, antall desimaler, verdiområde, kommentar, kodeliste,
    basert på gitt datadokreferanse. 
    F.eks. $FOB/person/arkiv/personfil/g2001/spes_reg_type

    
    Args:
        var_ref: The file path, plus the variable name in the file.
        
    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("datadok", "GetContextVariableByReference", var_ref)

def datadok_file_description_by_id(file_id: int | str) -> OrderedDict[str, Any]:
    """Rutinen skal returnere én filbeskrivelse basert på gitt filbeskrivelse Id eller urn. 
    
    F.eks 1288400 eller urn:ssb:dataset:datadok:1288400
    
    Args:
        file_id: The id the file.
        
    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("datadok", "GetFileDescriptionById", file_id)

def datadok_file_description_by_path(file_path: str) -> OrderedDict[str, Any]:
    """Rutinen skal returnere én filbeskrivelse basert på gitt Datadok sti. 
    
    F.eks. $FOB/person/arkiv/personfil/g2001.
    
    Args:
        file_path: The path to check for datadok-files, usually using the dollar-stamme, and without file-extension.
        
    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    
    return try_zeep_serialize_path(file_path,
                                   tbmd_service="datadok",
                                   operation="GetFileDescriptionByPath", )
    

    
    
    
    




