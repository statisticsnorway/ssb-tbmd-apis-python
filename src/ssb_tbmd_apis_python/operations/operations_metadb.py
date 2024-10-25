"""
GetCodelistById
Rutinen skal returnere én kodeliste basert på gitt kodeliste Id eller urn. F.eks 10013 eller urn:ssb:codelist:metadb:10013

GetCodelists
Rutinen skal returnere en oversikt over hvilke kodelister som finnes i metadb.

GetContextVariableById
Rutinen skal returnere én variabel med alle attributter (navn, fullt navn, datatype, lengde, desimaler, variabeltype, gyldig fra/til, datoformat, datering, endring, kodeliste og vardokreferanse) basert på gitt variabel Id eller urn. Variablene må være godkjent for Internett. F.eks 14739 eller urn:ssb:contextvariable:metadb:14739

GetDataDescriptionById
Rutinen skal returnere én tabell med alle attributter (overtema, subtema, navn, beskrivelse, gyldig fra/til og alle variabler) basert på gitt tabell Id eller urn. Tabellen og variablene må være godkjent for Internett. F.eks tabell id 11518 eller urn:ssb:dataset:metadb:11518

GetEventHistoryStructureById
Rutinen skal returnere ett prosjekt med tilhørende overtema, subtema, tabeller og variabler basert på gitt prosjekt Id eller urn. Gyldige prosjekt Id'er er 1001 og 1004. Gyldige urn'er er urn:ssb:project:metadb:1001 og urn:ssb:project:metadb:1004"""


from collections import OrderedDict
from ssb_tbmd_apis_python.zeep_client import get_zeep_client
import zeep
import pandas as pd


def metadb_codelist_by_id():
    pass

def metadb_codelists():
    pass

def metadb_context_variable_by_id():
    pass

def metadb_description_by_id():
    pass

def metadb_event_history_structure_by_id():
    pass