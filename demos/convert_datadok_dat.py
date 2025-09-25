# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: ssb-tbmd-apis-python
#     language: python
#     name: ssb-tbmd-apis-python
# ---

# %%
from ssb_tbmd_apis.imports.datadok_open_flatfile import datadok_open_flatfile_from_path

# %%
df = datadok_open_flatfile_from_path(
    "/ssb/stamme01/utd_pii/gjfor_vgo/arkiv/5s6y/g2017g2023"
)

# %%
df["grunnskolepoeng"]

# %%
df.info()

# %%
