# caa-group03

## TODO:

1. Add prices to .csv file and change load script (Ognjen)
2. Create flask project with neo4j query example (Rene)
3. Label known address owners (Maria)
4. BitPanda Pro analysis (Mimi)
5. 

## NEO4J Setup

Start the neo4j DB with following steps:

```bash
# pull image
docker pull neo4j:latest
# start the container
docker run --name testneo4j -p7474:7474 -p7687:7687 -d \
            -v $HOME/neo4j/data:/data -v $HOME/neo4j/logs:/logs -v $HOME/neo4j/import:/var/lib/neo4j/import -v $HOME/neo4j/plugins:/plugins \ 
            --env NEO4J_AUTH=neo4j/password  neo4j:latest
```
_Works for WSL or Bash terminal, for CMD/Powershell might need to replace $HOME variable._

### Importing data

```bash
# copy the csv file 
docker cp datasource/etherscan-best-pub-trans-all.csv <name_of_neo4j_container>:/var/lib/neo4j/import
```

In the neo4j console use the following command to load the data:

```cypher
LOAD CSV FROM "file:///etherscan-best-pub-trans.csv" as row
MERGE (a:Address {value:row[4]})
MERGE (b:Address {value:row[5]})
MERGE (a)-[:Transaction {tx_hash:row[0], block_num:row[1], unix_ts: row[2], datetime:row[3], amount:row[6], method:row[7]}]->(b)
RETURN row[4], row[5], row[0]
```


### Display the data
```cypher
MATCH (a:Address)<-[t:Transaction]-(b:Address)
WHERE a.value=~'0x0000.*' //to avoid large graph displays
return a,t,b
```

