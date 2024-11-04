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
from ssb_tbmd_apis.exports.migrerdok import save_migrerdok_for_flatfile, get_colnames_from_migrerdok
from ssb_tbmd_apis.exports.migrermetadb import save_metadb_vars
from ssb_tbmd_apis.exports.migrervar import save_vardok_variables_belong_section

# %%
path = "$UTD/nudb/arkiv/vg_vitnemal/g2002"

# %%
migrer_path = save_migrerdok_for_flatfile("$UTD_PII/nudb/arkiv/vg_vitnemal/g2001g2010", overwrite=True)

# %%
import glob
paths = (glob.glob("/ssb/stamme01/utd_pii/nudb/arkiv/**/**/*.dat", recursive=True) +
         glob.glob("/ssb/stamme01/utd_pii/nudb/arkiv/**/**/*.txt", recursive=True))
for path in paths[:50]:
    try:
        save_migrerdok_for_flatfile(path, overwrite=True)
    except:
        print(f"Couldnt find script for {path}")

# %%
