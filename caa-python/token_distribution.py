import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Define a converter for the "Balance" column
converters = {
    'Balance': lambda x: pd.to_numeric(x.replace(',', ''))
}
holders = pd.read_csv('../datasource/token_holders.csv', converters=converters)
exchanges = pd.read_csv('../datasource/labeled_sorted_addresses.csv')

# exclude this address due to unknown category
holders = holders[holders['HolderAddress'] != '0xcdbf58a9a9b54a2c43800c50c7192946de858321']

holders = holders.merge(exchanges[['address', 'nameTag']], left_on='HolderAddress', right_on='address', how='left')

holders['isExchange'] = ~holders['nameTag'].isna()
holders['TokenHolderType'] = np.where(holders['isExchange'], 'Exchange', 'Private Wallet')

distribution = holders.groupby('TokenHolderType')['Balance'].sum()

total = distribution.sum()
distribution_percent = distribution / total * 100

print(distribution_percent)

plt.figure(figsize=(10, 6))
ax = sns.barplot(x=distribution_percent.index, y=distribution_percent.values)
plt.title('Distribution of BEST Tokens')
plt.xlabel('Token Holder Type')
plt.ylabel('Percentage (%)')

for p in ax.patches:
    ax.annotate(format(p.get_height(), '.1f'),
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center',
                xytext=(0, 9),
                textcoords='offset points')

plt.savefig("../visualization/private_exchange_distr.png")
plt.show()
