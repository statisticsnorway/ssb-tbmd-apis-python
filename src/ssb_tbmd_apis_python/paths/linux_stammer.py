import os

def linux_stammer(insert_environ: bool = False) -> dict[str, str]:
    """Manually load the "linux-forkortelser" in as dict.

    If the function can find the file they are shared in.

    Args:
        insert_environ: Set to True if you want the dict to be inserted into the
            environment variables (os.environ).

    Returns:
        dict[str, str]:  The "linux-forkortelser" as a dict

    Raises:
        ValueError: If the stamme_variabel file is wrongly formatted.
    """
    stm: dict[str, str] = {}
    with open("/etc/profile.d/stamme_variabel") as stam_var:
        for line in stam_var:
            line = line.strip()
            if line.startswith("export") and "=" in line:
                line_parts = line.replace("export ", "").split("=")
                if len(line_parts) != 2:
                    raise ValueError("Too many equal-signs?")
                first: str = line_parts[0]  # Helping mypy
                second: str = line_parts[1]  # Helping mypy
                stm[first] = second
                if insert_environ:
                    os.environ[first] = second
    return stm