import os, glob
from collections import OrderedDict
from typing import Any
import zeep
from ssb_tbmd_apis.zeep_client import get_zeep_serialize
from ssb_tbmd_apis.paths.linux_stammer import linux_stammer
from ssb_tbmd_apis.tbmd_logger import logger

KNOWN_EXTENSIONS = ["", ".dat", ".txt"]

def try_zeep_serialize_path(path: str,
                            tbmd_service: str = "datadok",
                            operation: str = "GetFileDescriptionByPath",
                           ) -> OrderedDict[str, Any]:
    # Remove extension
    file_path = path.split(".")[0]
    # Swap for $-path
    stm = linux_stammer(flip=True)
    for k, v in stm.items():
        if file_path.startswith(k + os.sep):
            file_path = file_path.replace(k + os.sep, v + os.sep)
            if not file_path.startswith("$"):
                file_path = "$" + file_path
            logger.info(f"When looking in datadok, we will be using the dollar-stamme {v}: {file_path}")
            break
            
    # Remove PII at the start
    file_path = os.sep.join([file_path.split(os.sep)[0].replace("_PII", ""), *file_path.split(os.sep)[1:]])
    
    # Try without PII
    try:
        return get_zeep_serialize("datadok", "GetFileDescriptionByPath", file_path)
    except zeep.exceptions.Fault as e:
        logger.info(f"Couldnt find datadok entry at {file_path}. Looking in PII.")
    
    # Try with "PII"
    file_path = file_path.split(os.sep)[0] + "_PII/" + os.sep.join(file_path.split(os.sep)[1:])
    return get_zeep_serialize("datadok", "GetFileDescriptionByPath", file_path)



def look_for_file_on_disk(path: str) -> str:
    # Swap dollar sign
    first_part = path.split(os.sep)[0]
    if first_part.startswith("$"):
        first_part = first_part[1:]
    replace = linux_stammer().get(first_part, None)
    if replace is not None:
        path = os.sep.join([replace, *path.split(os.sep)[1:]])
        logger.info(f"When looking for file on disk, replaced {first_part} with {replace}: {path}")
    
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