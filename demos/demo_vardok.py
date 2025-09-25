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
from ssb_tbmd_apis.operations.operations_vardok import (
    vardok_concept_variables_by_name_def,
)

# %%
from ssb_tbmd_apis.operations.operations_vardok import vardok_concept_variables_by_owner

len(vardok_concept_variables_by_owner("360"))

# %% jupyter={"outputs_hidden": true}
vardok_concept_variables_by_owner("360")

# %% jupyter={"outputs_hidden": true}
vardok_concept_variables_by_name_def("nus2000")

# %%
from ssb_tbmd_apis.operations.operations_datadok import datadok_context_variable_by_id

# %%
datadok_context_variable_by_id("868823")

# %%
