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
    # Keep this small for readability
    monkeypatch.setattr(tv, "TIME_TRAVEL", 2)  # first_yr = 2021, then 2020

    p = Path("/root/dir/g2021g2022.dat")
    out = tv.period_variations_path(p)

    # The first block (first_yr = 2021) must start with the moving-window pair
    first_block_head = Path("/root/dir/g2021g2022")
    assert out[0] == first_block_head

    # Within the first block (first_yr=2021), we expect single-pair guesses with
    # decreasing second_yr before the 4-link variants. Check a few relative orders:
    idx_2021_2025 = out.index(Path("/root/dir/g2021g2025"))
    idx_2021_2024 = out.index(Path("/root/dir/g2021g2024"))
    idx_4link_2025 = out.index(Path("/root/dir/g2021g2022g2025g2026"))
    assert idx_2021_2025 < idx_2021_2024 < idx_4link_2025  # single-pair come before 4-link

    # When the next block starts (first_yr=2020), the *first* entry of that block
    # must be the moving-window pair for that block, i.e., g2020g2021; and it should
    # appear before any second_yr guesses in the same block.
    head_2020 = Path("/root/dir/g2020g2021")
    any_2020_2025 = Path("/root/dir/g2020g2025")
    assert head_2020 in out  # block exists
    assert any_2020_2025 in out  # and its second_yr guesses exist

    i_head_2020 = out.index(head_2020)
    i_2020_2025 = out.index(any_2020_2025)
    assert i_head_2020 < i_2020_2025  # block head precedes its second_yr guesses
