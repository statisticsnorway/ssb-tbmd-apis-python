import os
from pathlib import Path
from typing import Literal, overload


# Dependant on the flag flip there are two options for the return type
@overload
def linux_stammer(*, insert_environ: bool = False, flip: Literal[True]) -> dict[Path, str]: ...
@overload
def linux_stammer(*, insert_environ: bool = False, flip: Literal[False] = False) -> dict[str, Path]: ...


def linux_stammer(
    insert_environ: bool = False, flip: bool = False
) -> dict[str, Path] | dict[Path, str]:
    """Manually load the "linux-forkortelser" in as dict.

    Args:
        insert_environ: Set to True if you want the dict to be inserted into the
            environment variables (os.environ).
        flip: Set to True if you want to flip the dict, so that the keys are the
            values and the values are the keys. This is useful if you want to
            convert a path with a "linux-forkortelse" to the full path.

    Returns:
        dict[str, str]:  The "linux-forkortelser" as a dict

    Raises:
        ValueError: If the stamme_variabel file is wrongly formatted.
    """
    stm: dict[str, Path] = {}
    with open("/etc/profile.d/stamme_variabel") as stam_var:
        for line in stam_var:
            line = line.strip()
            if line.startswith("export") and "=" in line:
                line_parts = line.replace("export ", "").split("=")
                if len(line_parts) != 2:
                    raise ValueError("Too many equal-signs?")
                first: str = line_parts[0]  # Helping mypy
                second: Path = Path(line_parts[1])  # Helping mypy
                stm[first] = second
                if insert_environ:
                    os.environ[first] = str(second)
    if flip:
        stm_flip: dict[Path, str] = {v: k for k, v in stm.items()}
        return stm_flip
    return stm
