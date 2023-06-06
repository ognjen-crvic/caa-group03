from datetime import datetime
import pandas as pd

"""
    Merge price info with the blockchain data
"""

#PATH = "../datasource/bitpanda-ecosystem-token-price-history_2018-06-06_2023-06-05.csv"
PATH = "../datasource/etherscan-best-pub-trans-original.csv"
df = pd.read_csv(PATH)
df1 = pd.read_csv("../datasource/bitpanda-ecosystem-token-price-history_2018-06-06_2023-06-05.csv")


def convert_to_unix(date_string, date_format='%b-%d-%Y'):
    date_object = datetime.strptime(date_string, date_format)
    unix_timestamp = int(date_object.timestamp())
    return unix_timestamp


df["unix_timestamp"] = df["DateTime"].apply(lambda x: convert_to_unix(x[:10], date_format='%Y-%m-%d'))
df1["unix_timestamp"] = df1["Date"].apply(convert_to_unix)

print("len(df)", len(df))
print("len(df1)", len(df1))

merged_df = pd.merge(df, df1, on=("unix_timestamp"), how="left")

print("len(merged_df)", len(merged_df))

merged_df = merged_df.drop_duplicates(subset="Txhash")
merged_df = merged_df.rename(columns={"unix_timestamp": "block_timestamp"})
merged_df = merged_df.fillna(None)

print(merged_df.to_string)

merged_df.to_csv("../datasource/etherscan-best-pub-trans.csv", index=False, )