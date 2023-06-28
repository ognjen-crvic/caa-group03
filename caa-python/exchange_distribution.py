import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Converter for the "Balance" column
converters = {
    'Balance': lambda x: pd.to_numeric(x.replace(',', ''))
}

holders = pd.read_csv('../datasource/token_holders.csv', converters=converters)
exchanges = pd.read_csv('../datasource/labeled_sorted_addresses.csv')

# Exclude this address due to unknown category
holders = holders[holders['HolderAddress'] != '0xcdbf58a9a9b54a2c43800c50c7192946de858321']

holders = holders.merge(exchanges[['address', 'nameTag']], left_on='HolderAddress', right_on='address', how='left')


# different categories of token holders
def categorize_token_holders(row):
    if pd.isna(row['nameTag']):
        return 'Private Wallet'
    elif row['nameTag'].strip() in ['Bitpanda Exchange']:
        return 'Bitpanda'
    elif row['nameTag'].strip() in ['Uniswap V2:Best DEX']:
        return 'Uniswap V2 (DEX)'
    else:
        return 'Other Exchanges (CEX)'


holders['TokenHolderType'] = holders.apply(categorize_token_holders, axis=1)

# Filter out private wallets
holders = holders[holders['TokenHolderType'].isin(['Bitpanda', 'Uniswap V2 (DEX)', 'Other Exchanges (CEX)'])]

distribution = holders.groupby('TokenHolderType')['Balance'].sum()

print("Total tokens for each category:")
print(distribution)

total = distribution.sum()
distribution_percent = distribution / total * 100

print("\nPercentage distribution:")
print(distribution_percent)

# Plot distribution bar chart
plt.figure(figsize=(12, 6))
ax = sns.barplot(x=distribution_percent.index, y=distribution_percent.values)
plt.title('Distribution of BEST Tokens Among Exchanges')
plt.xlabel('Token Holder Type')
plt.ylabel('Percentage (%)')

# Use a logarithmic scale for the y-axis bc of small numbers
plt.yscale('log')

ax.set_yticks([0.001, 0.01, 0.1, 1, 10, 100])
ax.get_yaxis().set_major_formatter(plt.ScalarFormatter())

plt.savefig("../visualization/exchanges_only_distr.png")
plt.show()
