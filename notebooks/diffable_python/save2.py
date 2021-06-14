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
role_ids = ["RO141", "RO172", "RO98","RO197","RO107"]
dfs = [records_for_role(role_id) for role_id in role_ids]
df = pd.concat(dfs)

df=df.reset_index()

#Calculate overall cost for warfarin tablets for 3 months to end of Feb 2020 for TPP practices
sql='''
SELECT
  pct, practice, bnf_code, bnf_name, quantity_per_item,
  SUM(CASE WHEN month = '2020-01-01' THEN items ELSE 0 END) AS jan_2020_items,
  SUM(CASE WHEN month = '2021-01-01' THEN items ELSE 0 END) AS jan_2021_items
FROM
  ebmdatalab.hscic.raw_prescribing_normalised AS rx
WHERE
  month IN ('2021-01-01','2020-01-01')
  AND bnf_code LIKE '041003%'
GROUP BY
  pct, practice, bnf_code, bnf_name, quantity_per_item
'''
exportfile = os.path.join("..","data","adp_df.csv") #set path for data cache
oat_df = bq.cached_read(sql, csv_path=exportfile, use_cache=True) #save dataframe to csv
display(oat_df) #show dataframe as a table

test = pd.merge(df, oat_df, how="right", on=["Name", "pct"])

oat_df.dtypes

oat_df.reset_index()

from ebmdatalab import bq
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
role_ids = ["RO99", "RO198", "RO177"]
dfs_prac = [records_for_role(role_id) for role_id in role_ids]
df_prac = pd.concat(dfs_prac)

df_prac.head()

df_prac = pd.concat(dfs_prac)

df_prac.head()

oat_prac = oat_df.groupby(['practice'],as_index=False)

oat_df_small = oat_df['practice'].to_frame()

oat_df = oat_df_small.groupby(['practice'])

oat_df_small.head(5000)

#Calculate overall cost for warfarin tablets for 3 months to end of Feb 2020 for TPP practices
sql='''
SELECT
practice
FROM
  ebmdatalab.hscic.raw_prescribing_normalised AS rx
WHERE
  month IN ('2021-01-01','2020-01-01')
  AND bnf_code LIKE '041003%'
GROUP BY
 practice
'''
exportfile = os.path.join("..","data","oat_prac_df.csv") #set path for data cache
oat_prac_df = bq.cached_read(sql, csv_path=exportfile, use_cache=True) #save dataframe to csv
display(oat_prac_df) #show dataframe as a table

for index, row in oat_prac_df:
    print(row)

i = 0
#new_df = pandas.DataFrame(columns = ['a','b','c','d'])
for index,row in oat_prac_df.iterrows():
    url = 'https://directory.spineservices.nhs.uk/ORD/2-0-0/organisations/'
    d = '{ + row['practice'] + '}'
   # j = json.loads(d)
   # response = requests.post(url,json = j)

   # data = response.json()
   # for new_data in data['c']:
      #  new_df.loc[i] = [row['a'],row['b'],row['c'],new_data]
        i += 1


# +
def build_request(row):
    return row['practice']}

request_bodies = oat_prac_df.apply(build_request, axis=1).tolist()

# +
    api_results = []
    for x in request_bodies:
        url ='https://directory.spineservices.nhs.uk/ORD/2-0-0/organisations/' + x
        request = requests.get(url)
        api_results.append(request.json())
# -


url = 'https://directory.spineservices.nhs.uk/ORD/2-0-0/organisations/M91013'

# +
r = requests.get(url)



    records = []
    url = f"https://directory.spineservices.nhs.uk/ORD/2-0-0/organisations/M91013?format=xml"
    rsp = requests.get(url)
    new_records = pd.read_xml(rsp)


# + active=""
# json = r.json()
# -

json

new_records

api_results

# +
dataframe = pd.DataFrame.from_dict(api_results, orient="index")
# -


dfdf = pd.read_json(api_results, orient='records')

print(pd.__version__)


