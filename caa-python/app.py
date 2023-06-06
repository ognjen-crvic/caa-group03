from flask import Flask
from neo4j import GraphDatabase, Result
from pandas import DataFrame
from py2neo import Graph
from py2neo.cypher import Cursor
from graphdatascience import GraphDataScience

app = Flask(__name__)

HOST = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "password"


# Use neo4j (GraphDatabase)
@app.route('/example1')
def example_1():
    _example: Example = Example(HOST, USER, PASSWORD)
    _example.close()
    return _example.print_example()


# Use py2neo
@app.route('/example2')
def example_2():
    _example_graph: Graph = Graph(HOST, auth=(USER, PASSWORD))
    res: Cursor = _example_graph.run("MATCH (a:Address)<-[t:Transaction]-(b:Address) "
                                     "WHERE a.value=~'0x0000.*' "
                                     "return a,t,b")
    return res.data()  # get JSON-serializable data for testing


# Use graphdatascience
@app.route('/example3')
def example_3():
    gds: GraphDataScience = GraphDataScience(HOST, auth=(USER, PASSWORD))
    df: DataFrame = gds.run_cypher("MATCH (a:Address)<-[t:Transaction]-(b:Address) "
                                   "WHERE a.value=~'0x0000.*' "
                                   "return a,t,b")
    return df.to_json()


class Example:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.driver.verify_connectivity()

    def close(self):
        self.driver.close()

    def print_example(self):
        with self.driver.session() as session:
            res = session.execute_read(self._read_example_query)
        return res

    @staticmethod
    def _read_example_query(tx):
        res: Result = tx.run("MATCH (a:Address)<-[t:Transaction]-(b:Address) "
                             "WHERE a.value=~'0x0000.*' "
                             "return a,t,b")
        return res.data()  # get JSON-serializable data for testing


if __name__ == '__main__':
    app.run()
