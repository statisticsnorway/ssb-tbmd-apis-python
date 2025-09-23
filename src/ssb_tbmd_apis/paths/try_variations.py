import datetime
import glob
import os
from collections import OrderedDict
from pathlib import Path
from typing import Any

import zeep

from ssb_tbmd_apis.paths.linux_stammer import linux_stammer
from ssb_tbmd_apis.tbmd_logger import logger
from ssb_tbmd_apis.zeep_client import get_zeep_serialize

KNOWN_EXTENSIONS = ["", ".dat", ".txt"]
TIME_TRAVEL = 20


def try_zeep_serialize_path(
    path: str,
    tbmd_service: str = "datadok",
    operation: str = "GetFileDescriptionByPath",
) -> tuple[OrderedDict[str, Any], Path]:
    """Try many different paths to get the file description from the datadok API using the provided path as a starting point.

    Args:
        path: Path to the file.
        tbmd_service: The TBMD service to use (default is "datadok").
        operation: The operation to perform (default is "GetFileDescriptionByPath").

    Returns:
        tuple: A tuple containing the file description and the path.

    Raises:
        FileNotFoundError: If the file description cannot be found.
    """
    # Remove extension
    file_path = path.split(".")[0]
    # Swap for $-path
    stm = linux_stammer(flip=True)
    for k, v in stm.items():
        if file_path.startswith(k + os.sep):
            file_path = file_path.replace(k + os.sep, v + os.sep)
            if not file_path.startswith("$"):
                file_path = "$" + file_path
            logger.info(
                f"When looking in datadok, we will be using the dollar-stamme {v}: {file_path}"
            )
            break

    # Remove PII at the start
    file_path = os.sep.join(
        [file_path.split(os.sep)[0].replace("_PII", ""), *file_path.split(os.sep)[1:]]
    )

    # Try without PII
    variations = period_variations_path(file_path)
    for variation in variations:
        try:
            return get_zeep_serialize(
                "datadok", "GetFileDescriptionByPath", variation
            ), Path(variation)
        except zeep.exceptions.Fault as e:
            logger.info(f"Couldnt find datadok entry at {variation}.: {e}")

    # Try with "PII"
    file_path = (
        file_path.split(os.sep)[0] + "_PII/" + os.sep.join(file_path.split(os.sep)[1:])
    )
    variations = period_variations_path(file_path)
    for variation in variations:
        try:
            return get_zeep_serialize(
                "datadok", "GetFileDescriptionByPath", variation
            ), Path(variation)
        except zeep.exceptions.Fault as e:
            logger.info(f"Couldnt find datadok entry at {variation}: {e}")

    raise FileNotFoundError(f"Failed looking for path in datadok-api: {path}")


def swap_dollar_sign(path: str | Path) -> Path:
    """Swap the dollar sign in the path with the corresponding path from linux_stammer.

    Args:
        path: Path to the file.

    Returns:
        Path: The modified path with the dollar sign swapped.

    Raises:
        TypeError: If the path is not a string or a Path object.
    """
    if isinstance(path, str):
        outpath = Path(path)
    elif isinstance(path, Path):
        outpath = path
    else:
        raise TypeError("Path in is not a str or pathlib.Path.")

    first_part = outpath.parts[0]
    if first_part.startswith("$"):
        first_part = first_part[1:]
    replace = linux_stammer().get(first_part, None)
    if replace is not None:
        outpath = Path(replace) / Path(*outpath.parts[1:])
    return outpath


def look_for_file_on_disk(path: str) -> str:
    """Look for a file on disk using various methods.

    Args:
        path: Path to the file.

    Returns:
        str: The path to the discovered file.

    Raises:
        FileNotFoundError: If the file cannot be found.
    """
    # Swap dollar sign
    path = swap_dollar_sign(path)

    # Attempt one, look for specific file
    if os.path.isfile(path):
        logger.info(f"Discovered file to open at {path}.")
        return path

    # Attempt two, look for common file extensions
    path_no_ext = path.rsplit(".", 1)[0]
    for ext in KNOWN_EXTENSIONS:
        check_path = path_no_ext + ext
        if os.path.isfile(check_path):
            logger.info(f"Discovered file to open at {check_path}.")
            return check_path

    # Attempt three, look to see if we can find single match using glob
    glob_result = glob.glob(path_no_ext + "*")
    if len(glob_result) == 1:
        logger.info(f"Discovered file to open at {glob_result[0]}.")
        return glob_result[0]
    else:
        f"Too many files discovered (more than one): {glob_result}"

    # Attempt four, flip pii
    path_parts = path_no_ext.split(os.sep)
    if path_parts[3].endswith("_pii"):
        path_parts[3] = path_parts[3][:-4]
    else:
        path_parts[3] += "_pii"
    glob_result = glob.glob(os.sep.join(path_parts) + "*")
    if len(glob_result) == 1:
        logger.info(f"Discovered file to open at {glob_result[0]}.")
        return glob_result[0]
    else:
        f"Too many files discovered (more than one): {glob_result}"

    raise FileNotFoundError("Cant find single file with that path on local drive.")


def period_variations_path(path: str) -> list[str]:
    """Generate variations of the path based on periods in the filename.

    Args:
        path: Path to the file.

    Returns:
        list[str]: List of variations of the path.
    """
    # Find periods in path
    periods = []
    temp_name = Path(path).stem
    while temp_name and temp_name[0] == "g" and temp_name[1:5].isdigit():
        periods += [int(temp_name[1:5])]
        temp_name = temp_name[5:]

    current_year = datetime.datetime.now().year

    variations = []
    # Build guesses for paths with single yead
    if len(periods) == 1:
        # Check back 20 years
        for first_yr in range(periods[0], periods[0] - TIME_TRAVEL, -1):
            variations += [Path(path).parent / f"g{first_yr}{temp_name}"]
            for second_yr in range(current_year, first_yr, -1):
                variations += [
                    Path(path).parent / f"g{first_yr}g{second_yr}{temp_name}"
                ]

    # Build guesses for paths with 2 years
    elif len(periods) == 2:
        diff = periods[1] - periods[0]

        for first_yr in range(periods[0], periods[0] - TIME_TRAVEL, -1):
            variations += [
                Path(path).parent / f"g{first_yr}g{first_yr+diff}{temp_name}"
            ]
            for second_yr in range(current_year, first_yr, -1):
                variations += [
                    Path(path).parent / f"g{first_yr}g{second_yr}{temp_name}"
                ]
                variations += [
                    Path(path).parent
                    / f"g{first_yr}g{first_yr+diff}g{second_yr}g{second_yr+diff}{temp_name}"
                ]

    else:
        variations += [path]
        logger.warning(
            f"Dont know what to do with {len(periods)} periods in path. Not guessing much... Variations: {variations}"
        )

    return variations
