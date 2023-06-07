import collections
import pandas as pd
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt

df = pd.read_csv('../datasource/etherscan-best-pub-trans.csv')

# Create a directed graph due to transaction data
G = nx.from_pandas_edgelist(df, source="From", target="To", edge_attr="Quantity", create_using=nx.DiGraph())
print('Graph properties: ', G)
print('Number of nodes:', len(G.nodes))
print('Number of edges:', len(G.edges))
print('Average degree:', sum(dict(G.degree()).values()) / len(G.nodes))

# Degree analysis
degrees = [d for n, d in G.degree()]
degree_count = collections.Counter(degrees)
deg, count = zip(*degree_count.items())

#degree distribution
plt.figure(figsize=(8, 6))
plt.loglog(deg, count, 'o')
plt.title("Degree Distribution")
plt.ylabel("Count (log scale)")
plt.xlabel("Degree (log scale)")
plt.show()

# In and out-degree analysis
in_degrees = dict(G.in_degree())
out_degrees = dict(G.out_degree())
df_degrees = pd.DataFrame.from_dict(in_degrees, orient='index', columns=['in_degree'])
df_degrees['out_degree'] = pd.Series(out_degrees)
df_degrees.to_csv('degree_analysis.csv', index_label='address')

# in and out degree plot
in_values = sorted(set(in_degrees.values()))
out_values = sorted(set(out_degrees.values()))
in_hist = [list(in_degrees.values()).count(x) for x in in_values]
out_hist = [list(out_degrees.values()).count(x) for x in out_values]

plt.figure()
plt.plot(in_values, in_hist, 'ro-')
plt.plot(out_values, out_hist, 'bv-')
plt.legend(['In-degree', 'Out-degree'])
plt.xlabel('Degree')
plt.ylabel('Number of nodes')
plt.title('Nodes degree In-Out')
plt.show()

# Additional network analysis
print('Graph Density:', nx.density(G))
print('Number of strongly connected components:', nx.number_strongly_connected_components(G))

# Display graph
network = Network(notebook=True)
network.from_nx(G)
network.show('../visualization/network.html')

# Create gexf file to use it in Gephi tool for experiments
nx.write_gexf(G, '../visualization/network.gexf')

# Dataframe with top 10 nodes with most degrees
df_degrees['total_degree'] = df_degrees['in_degree'] + df_degrees['out_degree']
df_top10_degrees = df_degrees.sort_values(by='total_degree', ascending=False).head(10)
print("\nTop 10 nodes with highest degrees:\n", df_top10_degrees)