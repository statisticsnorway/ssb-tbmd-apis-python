# tests/paths/test_linux_stammer.py
from __future__ import annotations

import builtins
import io
import os
from collections.abc import Callable
from pathlib import Path

import pytest

from ssb_tbmd_apis.paths.linux_stammer import linux_stammer

STAMME_PATH = Path("/etc/profile.d/stamme_variabel")


def _patch_open_for_stamme(monkeypatch: pytest.MonkeyPatch, content: str) -> None:
    """Patch builtins.open so opening STAMME_PATH returns our StringIO."""
    real_open: Callable[..., object] = builtins.open

    def fake_open(file: str | os.PathLike, *args, **kwargs):  # type: ignore[override]
        # Compare as Path to be platform-neutral
        if Path(file) == STAMME_PATH:
            return io.StringIO(content)
        return real_open(file, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fake_open, raising=True)


def test_linux_stammer_basic(monkeypatch: pytest.MonkeyPatch) -> None:
    content = """
# comment
export UTDANNING=/ssb/stam/utdanning
export FOO=/bar/baz
not-an-export
export BAZ=/x/y/z
"""
    _patch_open_for_stamme(monkeypatch, content)

    result = linux_stammer()  # flip=False (default)
    assert result == {
        "UTDANNING": Path("/ssb/stam/utdanning"),
        "FOO": Path("/bar/baz"),
        "BAZ": Path("/x/y/z"),
    }
    for v in result.values():
        assert isinstance(v, Path)


def test_linux_stammer_flip(monkeypatch: pytest.MonkeyPatch) -> None:
    content = "export UTDANNING=/ssb/stam/utdanning\nexport FOO=/bar/baz\n"
    _patch_open_for_stamme(monkeypatch, content)

    result = linux_stammer(flip=True)
    assert result == {
        Path("/ssb/stam/utdanning"): "UTDANNING",
        Path("/bar/baz"): "FOO",
    }
    for k in result.keys():
        assert isinstance(k, Path)
    for v in result.values():
        assert isinstance(v, str)


def test_linux_stammer_inserts_environ(monkeypatch: pytest.MonkeyPatch) -> None:
    content = "export UTDANNING=/ssb/stam/utdanning\nexport FOO=/bar/baz\n"
    _patch_open_for_stamme(monkeypatch, content)

    for k in ("UTDANNING", "FOO"):
        os.environ.pop(k, None)

    result = linux_stammer(insert_environ=True)

    # Compare with OS-appropriate rendering
    assert os.environ["UTDANNING"] == str(Path("/ssb/stam/utdanning"))
    assert os.environ["FOO"] == str(Path("/bar/baz"))

    # Return mapping is still names -> Path
    assert result["UTDANNING"] == Path("/ssb/stam/utdanning")
    assert result["FOO"] == Path("/bar/baz")


def test_linux_stammer_ignores_non_export_and_missing_equals(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    content = """
export ONLY_THIS=/ok/path
export_missing_equals
random text
"""
    _patch_open_for_stamme(monkeypatch, content)

    result = linux_stammer()
    assert result == {"ONLY_THIS": Path("/ok/path")}


def test_linux_stammer_bad_format_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    content = "export BAD=one=two\n"
    _patch_open_for_stamme(monkeypatch, content)

    with pytest.raises(ValueError):
        linux_stammer()
