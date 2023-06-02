FROM neo4j:latest
LABEL name="caa-group03-neo4j"

EXPOSE 7474 7687

VOLUME %HOMEPATH%/neo4j/data:/data
VOLUME %HOMEPATH%/neo4j/logs:/logs
VOLUME %HOMEPATH%/neo4j/import:/var/lib/neo4j/import
VOLUME %HOMEPATH%/neo4j/plugins:/plugins

ENV NEO4J_AUTH=neo4j/password
