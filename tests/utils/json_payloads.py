from __future__ import annotations

import json
from collections import OrderedDict
from pathlib import Path
from typing import Any

TEST_DATA_FOLDER = Path("tests/data_test_json")


def to_ordered(obj: Any) -> Any:
    """Recursively convert dicts to OrderedDict (preserving insertion order)."""
    if isinstance(obj, dict):
        od: OrderedDict[str, Any] = OrderedDict()
        for k, v in obj.items():
            od[k] = to_ordered(v)
        return od
    if isinstance(obj, list):
        return [to_ordered(v) for v in obj]
    return obj


def load_ordered_json(path: str | Path) -> OrderedDict[str, Any]:
    """Load a JSON file and return a recursively-OrderedDict structure."""
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    result = to_ordered(data)
    # Help the type checker; we know top-level is a mapping here.
    return result  # type: ignore[return-value]


def ref_to_name(ref: str) -> str:
    """Turn a Datadok reference into a safe filename stem.

    Examples:
        "$FOB/person/arkiv/personfil/g2001/spes_reg_type"
        -> "FOB__person__arkiv__personfil__g2001__spes_reg_type"
    """
    name = ref.removeprefix("$")
    # Replace path separators with a readable token
    name = name.replace("/", "__")
    # Extra hardening: remove characters that are unfriendly on Windows, etc.
    forbidden = '<>:"\\|?*'
    for ch in forbidden:
        name = name.replace(ch, "_")
    # Avoid empty stems
    return name or "root"


def load_fixture(
    service: str,
    operation: str,
    name: str,
    base: Path = TEST_DATA_FOLDER,
) -> OrderedDict[str, Any]:
    """Load fixture JSON from tests/data_test_json/<service>/<operation>/<name>.json."""
    path = base / service / operation / f"{name}.json"
    return load_ordered_json(path)
