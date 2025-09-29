# tests/oracle_direct/test_oracle_paths.py
from __future__ import annotations

from typing import List, Tuple
import pytest

from ssb_tbmd_apis.oracle_direct import oracle_paths
from oracledb import Error as OraError


class _FakeOracleCM:
    """A fake Oracle context manager with execute/fetchmany API."""

    def __init__(self, db: str, batches: list[list[tuple[str, ...]]], queries_sink: list[str]) -> None:
        self.db = db
        self._batches = [list(batch) for batch in batches]
        self._queries_sink = queries_sink

    def __enter__(self) -> "_FakeOracleCM":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False

    def execute(self, query: str) -> None:
        self._queries_sink.append(query)

    def fetchmany(self, size: int) -> list[tuple[str, ...]]:
        if not self._batches:
            return []
        return self._batches.pop(0)


def _patch_oracle(monkeypatch: pytest.MonkeyPatch, batches: list[list[tuple[str, ...]]], queries_sink: list[str]) -> None:
    def _factory(*, db: str):
        return _FakeOracleCM(db=db, batches=batches, queries_sink=queries_sink)
    # Patch where Oracle is looked up
    monkeypatch.setattr(oracle_paths, "Oracle", _factory, raising=True)


def test_single_string_input_builds_uppercase_path_and_batches(monkeypatch: pytest.MonkeyPatch) -> None:
    batches = [
        [("$UTD/nudb/arkiv/avslutta/g2021g2022.dat",),
         ("$UTD/nudb/arkiv/avslutta/g2023g2024.dat",)],
        []
    ]
    queries: list[str] = []
    _patch_oracle(monkeypatch, batches=batches, queries_sink=queries)

    out = oracle_paths.paths_in_substamme("$utd/nudb", database="DWH")

    assert out == [
        "$UTD/nudb/arkiv/avslutta/g2021g2022.dat",
        "$UTD/nudb/arkiv/avslutta/g2023g2024.dat",
    ]
    assert len(queries) == 1
    q = queries[0]
    # Expect SINGLE '$' and no braces
    assert "'$UTD/nudb/arkiv/'" in q


def test_tuple_input_works_and_uses_same_code_path(monkeypatch: pytest.MonkeyPatch) -> None:
    batches = [[("$FOB/person/arkiv/avslutta/g2020g2021.dat",)], []]
    queries: list[str] = []
    _patch_oracle(monkeypatch, batches=batches, queries_sink=queries)

    out = oracle_paths.paths_in_substamme(("fob", "person"), database="DWH")
    assert out == ["$FOB/person/arkiv/avslutta/g2020g2021.dat"]
    assert len(queries) == 1
    # Expect SINGLE '$' and no braces
    assert "'$FOB/person/arkiv/'" in queries[0]


def test_list_of_pairs_produces_union_all_and_combines_results(monkeypatch: pytest.MonkeyPatch) -> None:
    batches = [[
        ("$FOB/person/arkiv/avslutta/g2020g2021.dat",),
        ("$UTD/nudb/arkiv/avslutta/g2021g2022.dat",),
    ]]
    queries: list[str] = []
    _patch_oracle(monkeypatch, batches=batches, queries_sink=queries)

    out = oracle_paths.paths_in_substamme([("fob", "person"), ("utd", "nudb")], database="DWH")
    assert out == [
        "$FOB/person/arkiv/avslutta/g2020g2021.dat",
        "$UTD/nudb/arkiv/avslutta/g2021g2022.dat",
    ]
    assert " UNION ALL " in queries[0]
    # Expect SINGLE '$' and no braces for both stammes
    assert "'$FOB/person/arkiv/'" in queries[0]
    assert "'$UTD/nudb/arkiv/'" in queries[0]


@pytest.mark.parametrize(
    "bad_input",
    [
        123,
        [("ok", "ok"), ("bad", 1)],
        ["not-a-tuple"],
        ("too", "many", "items"),
    ],
)
def test_type_errors_for_bad_input(bad_input, monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_oracle(monkeypatch, batches=[], queries_sink=[])
    with pytest.raises((TypeError, ValueError)):
        oracle_paths.paths_in_substamme(bad_input, database="DWH")
