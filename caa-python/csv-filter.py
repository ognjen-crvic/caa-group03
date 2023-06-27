import pandas as pd
from pandas import DataFrame

df: DataFrame = pd.read_csv("../datasource/etherscan-best-pub-trans-all.csv")

print(df.duplicated())
df = df.drop_duplicates(subset=["Txhash"])

print(df.duplicated())

df.to_csv("../datasource/etherscan-best-pub-trans.csv", index=False)
