from __future__ import annotations

from collections import OrderedDict
from typing import Any
from typing import Protocol

import pytest
from tests.utils.json_payloads import load_fixture
from tests.utils.json_payloads import ref_to_name

import ssb_tbmd_apis.operations.operations_datadok as ops_mod  # module to patch
from ssb_tbmd_apis.operations.operations_datadok import datadok_codelist_by_id
from ssb_tbmd_apis.operations.operations_datadok import datadok_codelist_by_reference


class _GetZeepSerialize(Protocol):
    def __call__(
        self, tbmd_service: str, operation: str, *args: str | int
    ) -> OrderedDict[str, Any]: ...


@pytest.mark.parametrize("codelist_id", [228589, "228589"])
def test_codelist_by_id_from_json(
    monkeypatch: pytest.MonkeyPatch, codelist_id: int | str
) -> None:
    # Load fixture (no hardcoded object-building):
    fake_payload: OrderedDict[str, Any] = load_fixture(
        "datadok", "GetCodelistById", "228589"
    )

    def fake_get_zeep_serialize(
        tbmd_service: str, operation: str, *args: str | int
    ) -> OrderedDict[str, Any]:
        assert tbmd_service == "datadok"
        assert operation == "GetCodelistById"
        # We accept either str or int id, mirroring the function signature:
        assert args and str(args[0]) == "228589"
        return fake_payload

    # Patch where the function is looked up:
    monkeypatch.setattr(
        ops_mod, "get_zeep_serialize", fake_get_zeep_serialize, raising=True
    )

    # Exercise
    result = datadok_codelist_by_id(codelist_id)

    # Schema-style checks (no field construction or brittle value assertions):
    assert isinstance(result, OrderedDict)
    assert "CodelistMeta" in result
    assert "Codes" in result
    assert "id" in result and str(result["id"]).endswith(":228589")

    codes = result["Codes"].get("Code")
    assert isinstance(codes, list) and len(codes) >= 1
    first = codes[0]
    assert isinstance(first, (dict, OrderedDict))
    # spot-check presence of typical fields, without pinning to specific values
    for key in ("CodeValue", "CodeText", "id"):
        assert key in first


def test_codelist_by_reference_from_json(monkeypatch: pytest.MonkeyPatch) -> None:
    ref = "$FOB/person/arkiv/personfil/g2001/spes_reg_type"
    name = ref_to_name(ref)
    fake_payload: OrderedDict[str, Any] = load_fixture(
        "datadok", "GetCodelistByReference", name
    )

    def fake_get_zeep_serialize(
        tbmd_service: str, operation: str, *args: str | int
    ) -> OrderedDict[str, Any]:
        assert tbmd_service == "datadok"
        assert operation == "GetCodelistByReference"
        assert args == (ref,)
        return fake_payload

    monkeypatch.setattr(
        ops_mod, "get_zeep_serialize", fake_get_zeep_serialize, raising=True
    )

    # Exercise
    result = datadok_codelist_by_reference(ref)

    # Verify shape & a few key fields
    assert isinstance(result, OrderedDict)
    assert "CodelistMeta" in result
    assert "Codes" in result and "Code" in result["Codes"]
    codes = result["Codes"]["Code"]
    assert isinstance(codes, list) and len(codes) >= 1
    # Spot checks
    assert result["CodelistMeta"]["Title"]["_value_1"] == "spes_reg_type"
    assert codes[0]["CodeValue"] in {"0", "1"}
