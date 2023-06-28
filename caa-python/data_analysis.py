import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from scipy.stats import pearsonr

plot_configs = [
    {
        "x_column_name": "Date",
        "y_column_name": "PrivateWalletUsage",
        "x_label": "Date",
        "y_label": "Private Wallet Usage",
        "plot_title": "Private Wallet Usage over Time"
    },
    {
        "x_column_name": "Date",
        "y_column_name": "Volume",
        "x_label": "Date",
        "y_label": "Volume",
        "plot_title": "Volume over Time"
    }
]


def make_line_plot(data: pd.DataFrame, plot_name: str, plot_title: str, plot_configs: list):
    data['Date'] = pd.to_datetime(data['Date'], format='mixed')

    rc_config = {
        "font.size": 12,
        'figure.figsize': (12, 10),
    }
    mpl.rcParams.update(rc_config)
    mpl.rcParams['axes.linewidth'] = 2
    fig, ax = plt.subplots(nrows=len(plot_configs))

    color_palette = sns.color_palette("Dark2", 20)
    sns.set_palette(palette=color_palette)
    sns.set_style(style="ticks")

    for idx, plot_config in enumerate(plot_configs):
        x_column_name = plot_config["x_column_name"]
        y_column_name = plot_config["y_column_name"]
        x_label = plot_config["x_label"]
        y_label = plot_config["y_label"]
        fig_title = plot_config["plot_title"]

        plot = sns.lineplot(data=data, x=data[x_column_name], y=data[y_column_name],
                            ax=ax[idx], color=color_palette[idx])

        ax[idx].set_xlabel(xlabel=x_label)
        ax[idx].set_ylabel(ylabel=y_label)
        ax[idx].set_title(fig_title)

    fig.suptitle(plot_title, fontsize=20)

    plt.tight_layout()
    plt.savefig(plot_name)
    plt.show()
    plt.close()


def plot_and_calculate_corr(data, x, y, title, save_filename):
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.tick_params(labelsize=12)
    sns.scatterplot(data=data, x=x, y=y)
    plt.xlabel(x, fontsize=12)
    plt.ylabel(y, fontsize=12)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(save_filename)
    plt.show()
    plt.close()

    corr, p_value = pearsonr(data[x], data[y])
    print(f'Pearson correlation: {corr}')


transactions = pd.read_csv('../datasource/etherscan-best-pub-trans.csv')
addresses = pd.read_csv('../datasource/labeled_sorted_addresses.csv')
exchange_addresses = addresses['address'].tolist()

transactions['Date'] = pd.to_datetime(transactions['DateTime'])
transactions['Volume'] = pd.to_numeric(transactions['Volume'], errors='coerce')
transactions['Close'] = pd.to_numeric(transactions['Close'], errors='coerce')
transactions.set_index('Date', inplace=True)

transactions['Volume'] = transactions['Volume'].interpolate(method='time')

transactions = transactions.dropna(subset=['Close'])

transactions = transactions[~transactions['From'].isin(exchange_addresses)]
transactions = transactions[~transactions['To'].isin(exchange_addresses)]

transactions.reset_index(inplace=True)

counts = transactions.groupby(['Date', 'From']).size().reset_index(name='PrivateWalletUsage')

transactions = pd.merge(transactions, counts, how='left', on=['Date', 'From'])

transactions['PrivateWalletUsage'].fillna(0, inplace=True)

transactions.set_index('Date', inplace=True)

plot_and_calculate_corr(transactions, "Close", "PrivateWalletUsage",
                        "Correlation between coin price and private wallet usage",
                        "../visualization/corr_price_wallets.png")

plot_and_calculate_corr(transactions, "Close", "Volume",
                        "Correlation between coin price and trading volume",
                        "../visualization/corr_price_volume.png")

make_line_plot(transactions.reset_index(), "../visualization/time_series_plots.png", "Time Series Analysis",
               plot_configs)
