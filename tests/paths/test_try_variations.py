# tests/paths/test_period_variations.py
from __future__ import annotations

from pathlib import Path
import datetime
import types
import pytest

import ssb_tbmd_apis.paths.try_variations as tv


class _FixedDateTime(datetime.datetime):
    @classmethod
    def now(cls, tz=None):  # type: ignore[override]
        # Freeze "current" year to 2025 for deterministic tests
        return cls(2025, 6, 15, tzinfo=tz)


@pytest.fixture(autouse=True)
def freeze_time_and_shrink(monkeypatch: pytest.MonkeyPatch):
    # Freeze tv.datetime.datetime.now() → 2025
    monkeypatch.setattr(tv.datetime, "datetime", _FixedDateTime)
    # Make the search space small for speed/readability
    monkeypatch.setattr(tv, "TIME_TRAVEL", 3)  # only 3 starting years


def test_single_period_variations_order_and_content():
    # g2022.dat → expect:
    #   g2022
    #   g2022g2025, g2022g2024, g2022g2023
    # then next block for g2021, then g2020 (TIME_TRAVEL=3)
    p = Path("/root/dir/g2022.dat")
    out = tv.period_variations_path(p)

    # All are Path under the same parent
    assert all(isinstance(x, Path) for x in out)
    assert all(x.parent == p.parent for x in out)

    expected_prefix = [
        Path("/root/dir/g2022"),
        Path("/root/dir/g2022g2025"),
        Path("/root/dir/g2022g2024"),
        Path("/root/dir/g2022g2023"),
        Path("/root/dir/g2021"),
        Path("/root/dir/g2021g2025"),
        Path("/root/dir/g2021g2024"),
        Path("/root/dir/g2021g2023"),
    ]
    assert out[: len(expected_prefix)] == expected_prefix

    # Ensure it eventually includes g2020 block due to TIME_TRAVEL=3
    assert Path("/root/dir/g2020") in out


def test_two_period_variations_order_and_content(monkeypatch: pytest.MonkeyPatch):
    # Keep the list compact and deterministic
    monkeypatch.setattr(tv, "TIME_TRAVEL", 2)  # first_yr: 2021, then 2020

    p = Path("/root/dir/g2021g2022.dat")
    out = tv.period_variations_path(p)

    # Block head for first_yr=2021 must be the first element
    head_2021 = Path("/root/dir/g2021g2022")
    assert out[0] == head_2021

    # Within the 2021 block, for each second_yr we see, the single variant must
    # appear before its corresponding 4-link variant.
    parent = p.parent

    def idx(path_str: str) -> int:
        return out.index(parent / path_str)

    # Check a few second years that may exist based on the frozen year (2025)
    pairs_to_check = [
        ("g2021g2025", "g2021g2022g2025g2026"),
        ("g2021g2024", "g2021g2022g2024g2025"),
        ("g2021g2023", "g2021g2022g2023g2024"),
        # When second_yr == 2022, the "single" equals the block head; still ensure
        # its 4-link comes after at least one occurrence of the single.
        ("g2021g2022", "g2021g2022g2022g2023"),
    ]

    # Only assert for entries that actually exist in the output
    for single, four in pairs_to_check:
        single_path = parent / single
        four_path = parent / four
        if single_path in out and four_path in out:
            assert idx(single) < idx(four)

    # The next block (first_yr=2020) should start after all g2021* entries.
    head_2020 = parent / "g2020g2021"
    assert head_2020 in out

    last_2021_idx = max(i for i, path in enumerate(out) if path.name.startswith("g2021"))
    assert out.index(head_2020) > last_2021_idx
