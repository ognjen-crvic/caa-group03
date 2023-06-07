import pandas as pd
import networkx as nx
from pyvis.network import Network

df = pd.read_csv('../datasource/etherscan-best-pub-trans.csv')

# Create a directed graph due to transaction data
G = nx.from_pandas_edgelist(df, source="From", target="To", edge_attr="Quantity", create_using=nx.DiGraph())
print('Graph properties: ', G)
print('Number of nodes:', len(G.nodes))
print('Number of edges:', len(G.edges))
print('Average degree:', sum(dict(G.degree).values()) / len(G.nodes))

# Degree analysis
degrees = sorted([d for n, d in G.degree()], reverse=True)
print(degrees)

#Display graph
network = Network(notebook=True)
network.from_nx(G)

network.show('../visualization/network.html')

#Create gexf file to use it in Gephi tool for experiments
nx.write_gexf(G, '../visualization/network.gexf')

