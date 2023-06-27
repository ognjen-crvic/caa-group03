import pandas as pd
from pandas import DataFrame

df: DataFrame = pd.read_csv("../datasource/etherscan-best-pub-trans.csv")
degree_2_df: DataFrame = pd.read_csv("../datasource/sorted_nodes.csv")

degree_3_df: DataFrame = pd.DataFrame(columns=degree_2_df.columns.array)
for row in degree_2_df.iterrows():
    row = row[1]
    if row[3] >= 3:
        degree_3_df.loc[len(degree_3_df)] = row

degree_4_df: DataFrame = pd.DataFrame(columns=degree_2_df.columns.array)
for row in degree_2_df.iterrows():
    row = row[1]
    if row[3] >= 4:
        degree_4_df.loc[len(degree_4_df)] = row

core_2_decomposed_df: DataFrame = pd.DataFrame(columns=df.columns.array)
for row in df.iterrows():
    row = row[1]
    if row[4] in degree_2_df["address"].values and row[5] in degree_2_df["address"].values:
        core_2_decomposed_df.loc[len(core_2_decomposed_df)] = row

core_2_decomposed_df.to_csv("../datasource/etherscan-best-pub-trans-2-core.csv", index=False)

core_3_decomposed_df: DataFrame = pd.DataFrame(columns=df.columns.array)
for row in df.iterrows():
    row = row[1]
    if row[4] in degree_3_df["address"].values and row[5] in degree_3_df["address"].values:
        core_3_decomposed_df.loc[len(core_3_decomposed_df)] = row

core_3_decomposed_df.to_csv("../datasource/etherscan-best-pub-trans-3-core.csv", index=False)

core_4_decomposed_df: DataFrame = pd.DataFrame(columns=df.columns.array)
for row in df.iterrows():
    row = row[1]
    if row[4] in degree_4_df["address"].values and row[5] in degree_4_df["address"].values:
        core_4_decomposed_df.loc[len(core_4_decomposed_df)] = row

core_4_decomposed_df.to_csv("../datasource/etherscan-best-pub-trans-4-core.csv", index=False)



