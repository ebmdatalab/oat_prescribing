# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import pandas as pd
import requests

role_call = ["RO141", "RO172"]
records = []
for role in role_call: 
    limit = 1000
    #records = []
    url = f"https://directory.spineservices.nhs.uk/ORD/2-0-0/organisations?PrimaryRoleId={role}&Limit={limit}"
    rsp = requests.get(url)
    print (url)
    new_records = rsp.json()["Organisations"]
    while new_records:
        for record in new_records:
            record["Role"] = role
            records.append(record)
        #records.extend(new_records)
            print(len(records))
        offset = str(len(records))
        url = f"https://directory.spineservices.nhs.uk/ORD/2-0-0/organisations?PrimaryRoleId={role}&Limit={limit}&Offset={offset}"
        rsp = requests.get(url)
        new_records = rsp.json()["Organisations"]
    print(role)
    df = pd.DataFrame.from_records(records)

df.head(5000)

# +

limit = 1000
def records_for_role(role_id):
    records = []
    url = f"https://directory.spineservices.nhs.uk/ORD/2-0-0/organisations?PrimaryRoleId={role_id}&Limit={limit}"
    rsp = requests.get(url)
    new_records = rsp.json()["Organisations"]
    while new_records:
        records.extend(new_records)
        print(len(records))
        offset = str(len(records))
        url = f"https://directory.spineservices.nhs.uk/ORD/2-0-0/organisations?PrimaryRoleId=RO172&Limit={limit}&Offset={offset}"
        rsp = requests.get(url)
        new_records = rsp.json()["Organisations"]
    return pd.DataFrame.from_records(records)
df = pd.concat([records_for_role("RO141"), records_for_role("RO172")])
# -

df.head(5000)



limit = 1000
def records_for_role(role_id):
    records = []
    url = f"https://directory.spineservices.nhs.uk/ORD/2-0-0/organisations?PrimaryRoleId={role_id}&Limit={limit}"
    rsp = requests.get(url)
    new_records = rsp.json()["Organisations"]
    while new_records:
        records.extend(new_records)
        print(len(records))
        offset = str(len(records))
        url = f"https://directory.spineservices.nhs.uk/ORD/2-0-0/organisations?PrimaryRoleId={role_id}&Limit={limit}&Offset={offset}"
        rsp = requests.get(url)
        new_records = rsp.json()["Organisations"]
    return pd.DataFrame.from_records(records)
df2 = pd.concat([records_for_role("RO141"), records_for_role("RO172")])

df2.head(5000)

limit = 1000
def records_for_role(role_id):
    records = []
    url = f"https://directory.spineservices.nhs.uk/ORD/2-0-0/organisations?PrimaryRoleId={role_id}&Limit={limit}"
    rsp = requests.get(url)
    new_records = rsp.json()["Organisations"]
    while new_records:
        records.extend(new_records)
        print(len(records))
        offset = str(len(records))
        url = f"https://directory.spineservices.nhs.uk/ORD/2-0-0/organisations?PrimaryRoleId={role_id}&Limit={limit}&Offset={offset}"
        rsp = requests.get(url)
        new_records = rsp.json()["Organisations"]
    return pd.DataFrame.from_records(records)
#df3 = pd.concat([records_for_role("RO141"), records_for_role("RO172")])
df3 = pd.concat([records_for_role({role_id})])


