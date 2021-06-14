# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# ### Changes to Opioid Addiction Treatment due to COVID-19

# The question has been asked, has there been any changes to opioid addiction treatment (OAT) prescribng due to the COVID-19 pandemic, such as
# - were patients on daily dispensed medicines were generally switched to weekly or fortnightly dispensing
# - were patients on methadone were switched to buprenorphine?
#
# Are we able to discern any information from this, either using the OpenPrescribing dataset or via OpenSAFELY?  By undertaking a brief review of the data held in OpenPrescribing we should be able to understand the limitations of both datasets, as:
# - OpenPrescribing holds prescribing from both primary care and other community commissioned services, such as Local Authority-commissioned OAT services
# - OpenSAFELY only holds data from primary care
# - What is the structure of OpenPrescribing data in relation to installment prescribing on prescriptions such as FP10(MDA)?

# + trusted=true
import pandas as pd
import os
from ebmdatalab import bq

# + trusted=true
#get prescribing data from BigQuery
sql ='''
#create subquery to produce single table with all different commissioned sites and organisations
WITH org_types AS
(SELECT site_code, site_name, org_code, org_name, org.region AS region, org.stp AS stp, org.org_type  FROM `ebmdatalab.richard.oat_orgs_all` AS org
INNER JOIN
`ebmdatalab.richard.oat_sites_all` AS site
ON
org.org_code = site.parent)

SELECT rx.pct, org_code, org_name, org_type, bnf.chemical AS chem_sub, RTRIM(bnf_name) as bnf_name, quantity_per_item,
SUM(CASE WHEN month = '2020-01-01' THEN items ELSE 0 END) AS jan_2020_items, # calculate January 2020 items
SUM(CASE WHEN month = '2021-01-01' THEN items ELSE 0 END) AS jan_2021_items # calculate January 2021 items
FROM ebmdatalab.hscic.raw_prescribing_normalised AS rx
INNER JOIN
org_types AS org
ON
rx.practice = org.site_code
INNER JOIN
hscic.bnf AS bnf
ON
rx.bnf_code = bnf.presentation_code
WHERE bnf_code LIKE '0410030%'
AND month IN ('2021-01-01','2020-01-01')
GROUP BY pct, org_code, org_name, org_type, chem_sub,  bnf_name, quantity_per_item
ORDER BY quantity_per_item
'''
exportfile = os.path.join("..","data","oat_df.csv") #set path for data cache
oat_df = bq.cached_read(sql, csv_path=exportfile, use_cache=True) #save dataframe to csv
display(oat_df) #show dataframe as a table

# + trusted=true
#create total volume quantities in df
oat_df["jan_2020_tot_quantity"] = oat_df["quantity_per_item"] * oat_df["jan_2020_items"]
oat_df["jan_2021_tot_quantity"] = oat_df["quantity_per_item"] * oat_df["jan_2021_items"]
# -

# ### What were total quantity differences between January 2020 and Jan 2021

# + trusted=true
#create change volume changes between Jan 2020 and Jan 2021
# create table to show which type of organisation prescribe OAT
oat_tot_df = oat_df.groupby(['chem_sub'])[["jan_2020_tot_quantity", "jan_2021_tot_quantity"]].sum()
display(oat_tot_df)
# -

# There appears to be a small increase in buprenorphine prescribing, although there is little change in methadone prescribing.

# ### Which organisations prescribed OAT?

# #### Absolute numbers

# + trusted=true
# create table to show which type of organisation prescribe OAT
oat_org_df = oat_df.groupby(['chem_sub','org_type'])[["jan_2020_tot_quantity", "jan_2021_tot_quantity"]].sum()
oat_org_df.unstack(0)
# -

# #### Percentages

# + trusted=true
percents_df = oat_org_df.groupby(level=0).apply(lambda x: 100 * x / (x.sum()))
percents_df.unstack(0)
# -

# As you can see from above, only about 25-30% of OAT prescribing takes place on a CCG-commissioned provider (i.e. primary care).  This means that the majority of prescribing is unlikely to have a record in OpenSAFELY.

# ### What quantities are prescribed?

# Using methadone 1mg/ml oral solution as an example, we can see what the data considers to be a "prescription", i.e. whether it is the daily installment dispensed to the patient, or whether it is the total quantity on a single FP10(MDA), which is usually for 14 days.

# + trusted=true
#create list of quantities of prescribing of methadone and physeptone liquid
meth_list =['Physeptone 1mg/ml oral solution sugar free', 'Methadone 1mg/ml oral solution sugar free','Methadone 1mg/ml oral solution']
meth_df = oat_df[oat_df['bnf_name'].isin(meth_list)].groupby(['quantity_per_item']).sum()
meth_df = meth_df.sort_values('jan_2021_items', ascending=False)
meth_df.head(20) # select top 20 quantities of items prescribed in January 2021

# -

# As per above, the 20 most common quantities prescribed in January 2021 are all quantities which appear to be divisible by 14, and are too high to be quantities for a single day's supply of methadone.  Consquently, it appears that OpenPrescribing data only holds the data for the entire prescription, not for daily installments.


