import pandas as pd
import matplotlib.pyplot as plt

exchange_df = pd.read_csv('../datasource/labeled_sorted_addresses.csv')
transactions_df = pd.read_csv('../datasource/etherscan-best-pub-trans.csv')

transactions_df['Quantity'] = pd.to_numeric(transactions_df['Quantity'].str.replace(',', ''))

bitpanda_addresses = exchange_df[exchange_df['nameTag'].str.contains('Bitpanda')]['address'].tolist()
bitpanda_transactions = transactions_df[
    transactions_df['From'].isin(bitpanda_addresses) | transactions_df['To'].isin(bitpanda_addresses)].copy()

bitpanda_transactions.loc[:, 'DateTime'] = pd.to_datetime(bitpanda_transactions['UnixTimestamp'], unit='s')
bitpanda_transactions.set_index('DateTime', inplace=True)

daily_volumes = bitpanda_transactions.resample('D')['Quantity'].sum()

plt.figure(figsize=(14, 7))
plt.plot(daily_volumes.index, daily_volumes.values)
plt.title('Daily Transaction Volumes for Bitpanda')
plt.xlabel('Date')
plt.ylabel('Volume')
plt.savefig("../visualization/active_trading.png")
plt.show()
plt.close()

# log scale
plt.figure(figsize=(14, 7))
plt.plot(daily_volumes.index, daily_volumes.values)
plt.title('Daily Transaction Volumes for Bitpanda')
plt.xlabel('Date')
plt.ylabel('Volume (log scale)')
plt.yscale('log')
plt.savefig("../visualization/active_trading_log.png")
plt.show()
plt.close()
