from neo4j import GraphDatabase
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

NEO4J_URI=os.getenv("NEO4J_URI")
NEO4J_USER=os.getenv("NEO4J_USER")
NEO4J_PASSWORD=os.getenv("NEO4J_PASSWORD")

df=pd.read_pickle("data/clean_movies.pkl")

driver=GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER,NEO4J_PASSWORD)
)

with driver.session() as s:
    for _,r in df.iterrows():
        s.run("""
        MERGE (m:Movie {id:$id})
        SET m.title=$title,m.year=$year,m.hitFlop=$hit
        """,id=r.imdbId,title=r.title,year=r.releaseYear,hit=r.hitFlop)

        for a in r.actor_list:
            s.run("""
            MERGE (a:Actor {name:$name})
            MERGE (m:Movie {id:$id})-[:ACTED_IN]->(a)
            """,name=a.strip(),id=r.imdbId)
