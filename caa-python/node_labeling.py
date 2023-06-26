import pandas as pd

df = pd.read_csv('../datasource/sorted_nodes.csv')
df2 = pd.read_csv('../datasource/all.csv')

df3 = pd.merge(df, df2, on=['address'])
df3.to_csv('../datasource/labeled_sorted_addresses.csv', index_label='index')
