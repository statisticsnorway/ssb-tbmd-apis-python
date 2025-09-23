"""Operations supported by the Vardok TBMD API."""

from collections import OrderedDict
from typing import Any

from ssb_tbmd_apis.zeep_client import get_zeep_serialize


def vardok_codelist_by_id(codelist_id: str | int) -> OrderedDict[str, Any]:
    """Rutinen skal returnere én kodeliste med gitt Id eller urn.

    F.eks 46 eller urn:ssb:codelist:vardok:46

    Args:
        codelist_id: The id of the codelist.

    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("vardok", "GetCodelistById", codelist_id)


def vardok_codelists() -> OrderedDict[str, Any]:
    """Rutinen skal returnere alle kodelistereferanser i Vardok.

    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("vardok", "GetCodelists")


def vardok_concept_variable_by_id(var_id: str | int) -> OrderedDict[str, Any]:
    """Rutinen skal returnere én variabel med alle attributter.

    Opprettet, sist endret, gyldig fra/til, navn, definisjon, statistisk enhet, intern kommentar,
    ekstern kommentar, sensitivitet, emnekode, kontaktperson, eierseksjon, statistikk, SSB kilde,
    ekstern kilde, ekstern referanse, stabasreferanse, beregning, id'er for lenkede variabler,
    datadokreferanser, kodelistereferanse.

    Basert på gitt variabel Id eller urn. Variablene må være godkjent for bruk internt.
    F.eks 123 eller urn:ssb:conceptvariable:vardok:123

    Args:
        var_id: The id of the variable.

    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("vardok", "GetConceptVariableById", var_id)


def vardok_concept_variables_by_approved(
    internal: bool = False,
) -> OrderedDict[str, Any]:
    """Rutinen skal returnere alle variablene som er godkjent for bruk eksternt eller internt.

    Nøkkelordene 'internet' må brukes for eksternt, og 'internal' for internt. OBS: Dette tar LANG tid.

    Args:
        internal: True if getting internal variables, False if external (internet).

    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    if internal:
        flag = "internal"
    else:
        flag = "internet"
    return get_zeep_serialize("vardok", "GetConceptVariablesByApproved", flag)


def vardok_concept_variables_by_external_source(
    var_id: str | int,
) -> OrderedDict[str, Any]:
    """Rutinen skal returnere det samme som GetConceptVariablesById for en gitt ekstern kilde.

    Opprettet, sist endret, gyldig fra/til, navn, definisjon, statistisk enhet, intern kommentar,
    ekstern kommentar, sensitivitet, emnekode, kontaktperson, eierseksjon, statistikk, SSB kilde,
    ekstern kilde, ekstern referanse, stabasreferanse, beregning, id'er for lenkede variabler,
    datadokreferanser, kodelistereferanse.

    Basert på gitt variabel Id eller urn. Variablene må være godkjent for bruk internt.
    F.eks 123 eller urn:ssb:conceptvariable:vardok:123

    Args:
        var_id: The id of the variable.

    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("vardok", "GetConceptVariablesByExternalSource", var_id)


def vardok_concept_variables_by_internal_source(
    var_id: str | int,
) -> OrderedDict[str, Any]:
    """Rutinen skal returnere det samme som GetConceptVariablesById for en oppgitt SSB-kilde.

    Opprettet, sist endret, gyldig fra/til, navn, definisjon, statistisk enhet, intern kommentar,
    ekstern kommentar, sensitivitet, emnekode, kontaktperson, eierseksjon, statistikk, SSB kilde,
    ekstern kilde, ekstern referanse, stabasreferanse, beregning, id'er for lenkede variabler,
    datadokreferanser, kodelistereferanse.

    Basert på gitt variabel Id eller urn. Variablene må være godkjent for bruk internt.
    F.eks 123 eller urn:ssb:conceptvariable:vardok:123

    Args:
        var_id: The id of the variable.

    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("vardok", "GetConceptVariablesByInternalSource", var_id)


def vardok_concept_variables_by_name_def(var_ref: str) -> OrderedDict[str, Any]:
    """Rutinen skal returnere id og variabeldefinisjon (se 2.1) etter å ha foretatt et fritekstsøk i navn og definisjon på variabel.

    Variablene må være godkjent for bruk internt

    Args:
        var_ref: The text to search for.

    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("vardok", "GetConceptVariablesByNameDef", var_ref)


def vardok_concept_variables_by_owner(section_id: str | int) -> OrderedDict[str, Any]:
    """Rutinen skal returnere det samme som GetConceptVariableById for en oppgitt eierseksjon.

    Args:
        section_id: The ID of the owning section.

    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("vardok", "GetConceptVariablesByOwner", section_id)


def vardok_concept_variables_by_statistical_unit(
    statistical_unit: str | int,
) -> OrderedDict[str, Any]:
    """Rutinen skal returnere det samme som GetConceptVariableById for en oppgitt telleenhet.

    Args:
        statistical_unit: The ID of the statistical unit.

    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize(
        "vardok", "GetConceptVariablesByStatisticalUnit", statistical_unit
    )


def vardok_concept_variables_by_subject_area(
    subject_area: str | int,
) -> OrderedDict[str, Any]:
    """Rutinen skal returnere det samme som GetConceptVariableById for en oppgitt telleenhet.

    Args:
        subject_area: The ID of the subject area.

    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize(
        "vardok", "GetConceptVariablesBySubjectArea", subject_area
    )


def vardok_version_by_concept_variable_id(
    variable_id: str | int,
) -> OrderedDict[str, Any]:
    """Rutinen skal levere alle versjoner av en variabel med alle attributter basert på gitt variabel Id eller urn.

    Versjoner av en variabel har samme navn, eier og statistisk enhet, men forskjellige gyldighetsperioder.

    F.eks 2007 urn:ssb:conceptvariable:vardok:2007

    Args:
        variable_id: The ID of the concept variable.

    Returns:
        OrderedDict: The serialized zeep OrderedDict.
    """
    return get_zeep_serialize("vardok", "GetVersionsByConceptVariableId", variable_id)
