"""
GetCodelistById
Rutinen skal returnere én kodeliste med gitt Id eller urn. F.eks 46 eller urn:ssb:codelist:vardok:46

GetCodelists
Rutinen skal returnere alle kodelistereferanser i Vardok

GetConceptVariableById
Rutinen skal returnere én variabel med alle attributter (opprettet, sist endret, gyldig fra/til, navn, definisjon, statistisk enhet, intern kommentar, ekstern kommentar, sensitivitet, emnekode, kontaktperson, eierseksjon, statistikk, SSB kilde, ekstern kilde, ekstern referanse, stabasreferanse, beregning, id'er for lenkede variabler, datadokreferanser, kodelistereferanse) basert på gitt variabel Id eller urn. Variablene må være godkjent for bruk internt. F.eks 123 eller urn:ssb:conceptvariable:vardok:123

GetConceptVariablesByApproved
Rutinen skal returnere alle variablene som er godkjent for bruk eksternt eller internt. Nøkkelordene 'internet' må brukes for eksternt, og 'internal' for internt. OBS: Dette tar LANG tid.

GetConceptVariablesByExternalSource
Rutinen skal returnere det samme som GetConceptVariablesById for en gitt ekstern kilde

GetConceptVariablesByInternalSource
Rutinen skal returnere det samme som GetConceptVariablesById for en oppgitt SSB-kilde

GetConceptVariablesByNameDef
Rutinen skal returnere id og variabeldefinisjon (se 2.1) etter å ha foretatt et fritekstsøk i navn og definisjon på variabel. Variablene må være godkjent for bruk internt

GetConceptVariablesByOwner
Rutinen skal returnere det samme som GetConceptVariableById for en oppgitt eierseksjon.

GetConceptVariablesByStatisticalUnit
Rutinen skal returnere det samme som GetConceptVariableById for en oppgitt telleenhet

GetConceptVariablesBySubjectArea
Rutinen skal returnere det samme som GetConceptVariablebyId fro en oppgitt emnekode

GetVersionsByConceptVariableId
Rutinen skal levere alle versjoner av en variabel med alle attributter basert på gitt variabel Id eller urn. Versjoner av en variabel har samme navn, eier og statistisk enhet, men forskjellige gyldighetsperioder. F.eks 2007 urn:ssb:conceptvariable:vardok:2007
"""

from collections import OrderedDict
from ssb_tbmd_apis_python.zeep_client import get_zeep_client
import zeep
import pandas as pd


def vardok_codelist_by_id():
    pass

def vardok_codelists():
    pass

def vardok_concept_variable_by_id():
    pass

def vardok_concept_variables_by_approved():
    pass

def vardok_concept_variables_by_external_source():
    pass

def vardok_concept_variables_by_internal_source():
    pass

def vardok_concept_variables_by_name_def():
    pass

def vardok_concept_variables_by_owner():
    pass

def vardok_concept_variables_by_statistical_unit():
    pass

def vardok_concept_variables_by_subject_area():
    pass

def vardok_version_by_concept_variable_id():
    pass