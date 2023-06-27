# caa-group03

## NEO4J Setup

Start the neo4j DB with following steps:

```bash
# pull image
docker pull neo4j:latest
# start the container
docker run --name testneo4j -p7474:7474 -p7687:7687 -d \
            -v $HOME/neo4j/data:/data -v $HOME/neo4j/logs:/logs -v $HOME/neo4j/import:/var/lib/neo4j/import -v $HOME/neo4j/plugins:/plugins \ 
            --env NEO4J_AUTH=neo4j/password --env NEO4JLABS_PLUGINS='["graph-data-science"]' neo4j:latest
```
_Works for WSL or Bash terminal, for CMD/Powershell might need to replace $HOME variable._

### Importing data

```bash
# copy csv files and other data
docker cp datasource testneo4j:/var/lib/neo4j/import
```

Go to : http://localhost:7474/browser/ after the docker container was successfully started.
In the neo4j console use the following command to load the data:

```cypher
LOAD CSV FROM "file:///datasource/etherscan-best-pub-trans-2-core.csv" as row
MERGE (a:Address {value:row[4]})
MERGE (b:Address {value:row[5]})
MERGE (a)-[:Transaction {tx_hash:row[0], block_num:row[1], unix_ts: row[2], datetime:row[3], amount:row[6], method:row[7], block_ts:row[8], open_price: row[10], close_price: row[13], low_price: row[11], high_price: row[12]}]->(b)
RETURN row[4], row[5], row[0]
```

```cypher
LOAD CSV FROM "file:///datasource/labeled_sorted_addresses.csv" as row_label
MATCH (n {value:row_label[1]})
WITH n, row_label[5] as label
SET n:label
RETURN n
```

### Display the data
```cypher
MATCH (a:Address)<-[t:Transaction]-(b:Address)
WHERE a.value=~'0x0000.*' //to avoid large graph displays
RETURN a,t,b
```
### Conda environment
Create a conda environment and install all the necessary dependencies using the provided env.yaml file:
```bash
conda env create -f environment.yml
```
After the environment is created, activate it using the following command:
```bash
conda activate caa_group03
```

