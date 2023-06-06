from flask import Flask
from neo4j import GraphDatabase, Result
from py2neo import Graph
from py2neo.cypher import Cursor

app = Flask(__name__)


# Use neo4j (GraphDatabase)
@app.route('/example1')
def example_1():
    _example: Example = Example("bolt://localhost:7687", "neo4j", "password")
    _example.close()
    return _example.print_example()


# Use py2neo
@app.route('/example2')
def example_2():
    _example_graph: Graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
    res: Cursor = _example_graph.run("MATCH (a:Address)<-[t:Transaction]-(b:Address) "
                                     "WHERE a.value=~'0x0000.*' "
                                     "return a,t,b")
    return res.data()  # get JSON-serializable data for testing


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
