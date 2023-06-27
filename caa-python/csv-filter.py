import pandas as pd
from pandas import DataFrame

print("test")

df: DataFrame = pd.read_csv("../datasource/etherscan-best-pub-trans-all.csv")
degree_2_df: DataFrame = pd.read_csv("../datasource/sorted_nodes.csv")

print(df.duplicated())
df = df.drop_duplicates(subset=["Txhash"])

print(df.duplicated())

df.to_csv("../datasource/etherscan-best-pub-trans.csv", index=False)

decomposed_df: DataFrame = pd.DataFrame(columns=df.columns.array)
for row in df.iterrows():
    row = row[1]
    if row[4] in degree_2_df["address"].values and row[5] in degree_2_df["address"].values:
        decomposed_df.loc[len(decomposed_df)] = row

print(decomposed_df)
decomposed_df.to_csv("../datasource/etherscan-best-pub-trans-2-core.csv")
