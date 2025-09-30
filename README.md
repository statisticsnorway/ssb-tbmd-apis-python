# SSB Tbmd Apis Python

[![PyPI](https://img.shields.io/pypi/v/ssb-tbmd-apis-python.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/ssb-tbmd-apis-python.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/ssb-tbmd-apis-python)][pypi status]
[![License](https://img.shields.io/pypi/l/ssb-tbmd-apis-python)][license]

[![Documentation](https://github.com/statisticsnorway/ssb-tbmd-apis-python/actions/workflows/docs.yml/badge.svg)][documentation]
[![Tests](https://github.com/statisticsnorway/ssb-tbmd-apis-python/actions/workflows/tests.yml/badge.svg)][tests]
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=statisticsnorway_ssb-tbmd-apis-python&metric=coverage)][sonarcov]
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=statisticsnorway_ssb-tbmd-apis-python&metric=alert_status)][sonarquality]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)][poetry]

[pypi status]: https://pypi.org/project/ssb-tbmd-apis-python/
[documentation]: https://statisticsnorway.github.io/ssb-tbmd-apis-python
[tests]: https://github.com/statisticsnorway/ssb-tbmd-apis-python/actions?workflow=Tests
[sonarcov]: https://sonarcloud.io/summary/overall?id=statisticsnorway_ssb-tbmd-apis-python
[sonarquality]: https://sonarcloud.io/summary/overall?id=statisticsnorway_ssb-tbmd-apis-python
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black
[poetry]: https://python-poetry.org/


# Tjenestebibliotek for metadata
Is an API built on top of Oracle in SSBs ON-prem environment for getting at metadata.\
This package is written for extracting the information where possible.

## Lenker ssb onprem:
- http://ws.ssb.no/Default.aspx
- http://trac.ssb.no/tbmd


## Installation

You can install _SSB Tbmd Apis Python_ via [pip] from [PyPI]:

```console
poetry add ssb-tbmd-apis-python
```

## Usage examples

Open a flatfile as a pandas dataframe with only the path to the datafile.
```python
from ssb_tbmd_apis.imports.datadok_open_flatfile import datadok_open_flatfile_from_path

df = datadok_open_flatfile_from_path(
    "/ssb/stam/utdanning/vgogjen/mappe/g2023"
)
```

Store a json of the "filbeskrivelse" - the metadata to interpret a "fixed-width-file" / "flatfile".
This stores the json next to the datafile, with the suffix "__MIGRERDOK.json"
```python
from ssb_tbmd_apis.exports.migrerdok import save_migrerdok_for_flatfile
migrer_path = save_migrerdok_for_flatfile(
    "$DOLLAR/team/archive/folder/g2001", overwrite=True
)
```

Get metadata from the old "vardok".
```python
from ssb_tbmd_apis.operations.operations_vardok import (
    vardok_concept_variables_by_name_def,
    vardok_concept_variables_by_owner
)

len(vardok_concept_variables_by_owner("360"))

print(vardok_concept_variables_by_owner("360"))

print(vardok_concept_variables_by_name_def("nus2000"))
```



Please see the [Reference Guide] for further details.


## License

Distributed under the terms of the [MIT license][license],
_SSB Tbmd Apis Python_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [Statistics Norway]'s [SSB PyPI Template].

[statistics norway]: https://www.ssb.no/en
[pypi]: https://pypi.org/
[ssb pypi template]: https://github.com/statisticsnorway/ssb-pypitemplate
[file an issue]: https://github.com/statisticsnorway/ssb-tbmd-apis-python/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/statisticsnorway/ssb-tbmd-apis-python/blob/main/LICENSE
[contributor guide]: https://github.com/statisticsnorway/ssb-tbmd-apis-python/blob/main/CONTRIBUTING.md
[reference guide]: https://statisticsnorway.github.io/ssb-tbmd-apis-python/reference.html
