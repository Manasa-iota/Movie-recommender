from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

driver=GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"),os.getenv("NEO4J_PASSWORD"))
)

def get_pagerank_candidates(imdbId):
    query="""
    MATCH (m:Movie {id:$imdbId})
    CALL gds.pageRank.stream(
      'movieGraph',
      {
        sourceNodes:[id(m)],
        maxIterations:20,
        dampingFactor:0.85
      }
    )
    YIELD nodeId, score
    RETURN gds.util.asNode(nodeId).id AS imdbId, score
    ORDER BY score DESC
    LIMIT 50
    """

    with driver.session() as s:
        result=s.run(query,imdbId=imdbId)
        return [(r["imdbId"],r["score"]) for r in result]
