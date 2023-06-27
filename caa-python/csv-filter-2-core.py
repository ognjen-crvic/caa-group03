import pandas as pd
from pandas import DataFrame

df: DataFrame = pd.read_csv("../datasource/etherscan-best-pub-trans.csv")
degree_2_df: DataFrame = pd.read_csv("../datasource/sorted_nodes.csv")

decomposed_df: DataFrame = pd.DataFrame(columns=df.columns.array)
for row in df.iterrows():
    row = row[1]
    if row[4] in degree_2_df["address"].values and row[5] in degree_2_df["address"].values:
        decomposed_df.loc[len(decomposed_df)] = row

print(decomposed_df)
decomposed_df.to_csv("../datasource/etherscan-best-pub-trans-2-core.csv", index=False)
