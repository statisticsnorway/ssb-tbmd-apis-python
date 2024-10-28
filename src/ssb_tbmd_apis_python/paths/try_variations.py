from zeep.exceptions import Fault

def try_path_possibilities(path: str, client) -> requests.Response:
    for try_path in _make_path_possibilites(path):
        try:
            response = datadok_get_file_description_by_path(try_path)
        except Fault as e:
            logger.info(f"Found no response in the API for path {try_path}")
    raise FileNotFoundError("Could not find the path you specified in the Datadok-api.")

    
def _make_path_possibilites(path: str) -> list[str]:
    pass