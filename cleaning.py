import pandas as pd
import numpy as np

df = pd.read_excel("ts20individual01byyear.xlsx", sheet_name='Table 1A', header = 1)

#print(df.head())
#print(df.info())

df.columns = df.columns.str.replace("–", '-')

for i in df.columns[2:]:
    df[i] = pd.to_numeric(df[i], errors='coerce')

#print(df.head())

df_list = np.split(df, df[df.isnull().all(1)].index)

for df in df_list:
    df = df.drop(df[df.isna().all(1)].index)
    print(df, '\n')
