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

# %% jupyter={"outputs_hidden": true}
from ssb_tbmd_apis_python import get_zeep_client
from ssb_tbmd_apis_python.zeep_client import ZeepClientManager

with ZeepClientManager(wsdl="http://ws.ssb.no/VardokService/VardokService.asmx?WSDL") as client:
    print(getattr(client.service, "GetConceptVariablesByNameDef")("nus2000"))

# %%
from ssb_tbmd_apis_python import datadok_file_description_by_path, datadok_vars_dataframe_by_path, dtypes_datadok_to_pandas

# %%
from ssb_tbmd_apis_python import get_zeep_client

# %%
path = "$UTD/gjfor_vgo/arkiv/5s6y/g2017g2023"

# %%
gjfor_ddok = datadok_file_description_by_path(path)

# %%
df = datadok_vars_dataframe_by_path(path)

# %%
from ssb_tbmd_apis_python.operations.operations_datadok import datadok_codelist_by_reference, datadok_context_variable_by_reference

# %% jupyter={"outputs_hidden": true}
datadok_context_variable_by_reference("$UTD/nudb/arkiv/avslutta/g2019g2020/spesund")

# %% jupyter={"outputs_hidden": true}
datadok_codelist_by_reference("$KULTMED/kulturbruk/arkiv/bruttoutvalg/g2021/Kino3a")

# %% jupyter={"outputs_hidden": true}
from ssb_tbmd_apis_python.operations.operations_vardok import vardok_concept_variables_by_owner
our_vars = vardok_concept_variables_by_owner(360)
our_vars

# %%
print(len(our_vars))
for var in our_vars:
    print(var["DataElementName"])
    print(var["NameGrp"]["Name"][-1]["_value_1"])
    print(var["DefinitionGrp"]["Definition"][0]["_value_1"])

# %%
from ssb_tbmd_apis_python.operations.operations_vardok import vardok_concept_variables_by_name_def
vardok_concept_variables_by_name_def("kilde")

# %%
dtypes_datadok_to_pandas(df)

# %%

# %%
