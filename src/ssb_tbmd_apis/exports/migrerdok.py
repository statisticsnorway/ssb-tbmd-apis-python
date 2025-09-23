import json
from pathlib import Path
from typing import Any

from fagfunksjoner.paths.versions import latest_version_path
from fagfunksjoner.paths.versions import next_version_path

from ssb_tbmd_apis.operations.operations_datadok import datadok_file_description_by_path
from ssb_tbmd_apis.paths.try_variations import swap_dollar_sign
from ssb_tbmd_apis.tbmd_logger import logger


def save_migrerdok_for_flatfile(
    flatfile: Path, version_up: bool = True, overwrite: bool = False
) -> Path:
    """Save datadok contents to a file, and version up if needed.

    Args:
        flatfile: Path to the flatfile.
        version_up: Whether to version up the file if it exists.
        overwrite: Whether to overwrite the file if it exists.

    Returns:
        Path: Path to the saved datadok file.

    Raises:
        OSError: If the file already exists, and overwrite is False.
    """
    # Get old meta from old datadok
    ddok_contents, ddok_save_path = datadok_file_description_by_path(flatfile)

    # Construct path
    ddok_path: Path = ddok_save_path.parent / (ddok_save_path.stem + "__MIGRERDOK_v1.json")
    ddok_path = swap_dollar_sign(ddok_path)

    # Write non-existing file / overwrite
    if not ddok_path.is_file() or overwrite:
        ddok_path.parent.mkdir(parents=True, exist_ok=True)
        with open(ddok_path, "w") as ddok_file:
            json.dump(ddok_contents, ddok_file, default=str)
        logger.info(f"Wrote datadok contents to {ddok_path}")
    # File exists, and we want to version up
    elif version_up:
        # Get highest available version path on disk
        path_highest_version = latest_version_path(str(ddok_path))

        # Check if content is the same
        with open(path_highest_version) as old_json:
            json_old = json.load(old_json)
        equal = deep_equal(
            json.dumps(json_old, default=str), json.dumps(ddok_contents, default=str)
        )

        # If different, bump highest available path, and write to empty path
        if not equal:
            bump_path = next_version_path(path_highest_version)
            with open(bump_path, "w") as ddok_file:
                logger.info(
                    f"Versioning up path, since we found existing file: {bump_path}"
                )
                json.dump(ddok_contents, ddok_file, default=str)
        else:
            logger.info(
                "Datadok contents equals old version, no point in versioning it up."
            )
    elif not overwrite:
        raise OSError(
            f"Not overwriting existing file {ddok_path}, set overwrite to True if you want to overwrite."
        )
    return ddok_path


def get_colnames_from_migrerdok(migrerdok: str | Path) -> list[str]:
    """Get column names from a migrerdok file.

    Args:
        migrerdok: Path to the migrerdok file.

    Returns:
        list[str]: List of column names.
    """
    path = swap_dollar_sign(migrerdok)
    with open(path) as migrerout:
        contents = json.load(migrerout)
    colnames = [x["Title"]["_value_1"] for x in contents["ContextVariable"]]
    return colnames


def deep_equal(elem1: Any, elem2: Any) -> bool | list[bool | Any]:
    """Recursively check equality between two elements, ignoring the order of lists.

    Args:
        elem1: The first element to compare.
        elem2: The second element to compare.

    Returns:
        bool: True if the elements are equal, otherwise False.
    """
    if not isinstance(elem1, type(elem2)):
        return False

    if isinstance(elem1, dict):
        if elem1.keys() != elem2.keys():
            return False
        return all(deep_equal(elem1[key], elem2[key]) for key in elem1)

    if isinstance(elem1, list):
        if len(elem1) != len(elem2):
            return False
        return sorted(
            deep_equal(item, elem2[i]) if isinstance(item, dict) else item
            for i, item in enumerate(elem1)
        )

    return bool(elem1 == elem2)
