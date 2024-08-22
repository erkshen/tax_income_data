import pandas as pd
import numpy as np

# read relevant file
df = pd.read_excel("ts20individual01byyear.xlsx", sheet_name='Table 1A', header = 1)

#print(df.head())
#print(df.info())

# cleaning columns and converting to numeric
df.columns = df.columns.str.replace("–", '-')

for i in df.columns[2:]:
    df[i] = pd.to_numeric(df[i], errors='coerce')

df.rename(columns={'Selected items1': 'Category','Unnamed: 1':'type'}, inplace=True)
#print(df.head())

# split into different dfs by empty rows, then remove said rows
df_list = np.split(df, df[df.isnull().all(1)].index)
#print(df_list.shape)

for d in df_list:
    d.dropna(axis=0, how='all', inplace=True)
    d.reset_index(inplace=True)

from pandas import ExcelWriter
import re

shorten = ['umber_of_individuals', 
           '-_', 
           'uction', 
           'and_', 
           'ribution',
           'mercial',
           '',
           ]
def save_xlsx(list_dfs, path):
    with ExcelWriter(path) as writer:
        list_dfs[0].to_excel(writer, 'individual_counts')
        sheet_names = ['individual_counts',]
        for d in list_dfs[1:]:
            #cleaning and shortening column names
            sheetname = re.sub(r'[ /]', '_', d['Category'][0])
            sheetname = re.sub(r'[:-]', '', sheetname)
            sheet_names.append(sheetname)
            for s in shorten:
                sheetname = sheetname.replace(s, '')
            sheetname = sheetname.replace('artnerships', 'ships')
            sheetname = sheetname.replace('management', 'mgmt')

            sheetname = sheetname[:31]

            d.drop(0, axis=0)
            d.to_excel(writer, sheetname)
        names = pd.DataFrame(sheet_names)
        names.to_excel(writer, 'full_names')

save_xlsx(df_list, 'split.xlsx')
