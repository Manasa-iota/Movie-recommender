HYBRID MOVIE RECOMMENDATION SYSTEM (GRAPH + EMBEDDINGS)
=====================================================

A hybrid movie recommendation system that combines semantic similarity using
transformer-based embeddings with graph-based ranking using Neo4j Personalized
PageRank to deliver accurate, explainable, and cold-start friendly recommendations.


FEATURES
--------
- Content-based recommendations using Indic-BERT embeddings
- Relationship-aware recommendations using Neo4j graph database
- Personalized PageRank for graph-based ranking
- Hybrid scoring combining graph importance and cosine similarity
- Cold-start support (no user history required)
- Modular and extensible architecture


SYSTEM ARCHITECTURE
-------------------
Movie Metadata
      ↓
Text Embeddings (Indic-BERT)
      ↓
Cosine Similarity  ------
                         → Hybrid Ranking → Top-K Recommendations
Neo4j Graph → PageRank ---


DATASET
-------
Each movie contains the following fields:

imdbId
title
releaseYear
releaseDate
genre
writers
actors
directors
sequel
hitFlop

Text used for embeddings:
title + genre + actors + directors


RECOMMENDATION STRATEGY
-----------------------

1. CONTENT-BASED FILTERING
- Movies are encoded into dense vectors using Indic-BERT
- Similarity between movies is computed using cosine similarity

2. GRAPH-BASED RECOMMENDATION (NEO4J)
Movies are modeled as a heterogeneous graph:

(Movie)-ACTED_IN->(Actor)
(Movie)-HAS_GENRE->(Genre)
(Movie)-DIRECTED_BY->(Director)
(Movie)-SEQUEL_OF->(Movie)

3. GRAPH ALGORITHM
- Personalized PageRank using Neo4j Graph Data Science
- Ranks movies based on structural importance relative to a given movie

4. HYBRID RANKING
Final score calculation:

FinalScore =
  0.7 × CosineSimilarity
+ 0.3 × PageRankScore


PROJECT STRUCTURE
-----------------
movie-recommender/

data/
  movies.csv
  clean_movies.pkl
  movies_with_embeddings.pkl

embeddings/
  build_embeddings.py

graph/
  load_neo4j.py
  neo4j_utils.py

recommend/
  recommend.py
  hybrid_recommend.py

eval/
  metrics.py

app.py
requirements.txt
.env
README.txt


SETUP INSTRUCTIONS
------------------

1. CREATE VIRTUAL ENVIRONMENT
python -m venv venv
venv\Scripts\activate   (Windows)
source venv/bin/activate (Linux/Mac)

2. INSTALL DEPENDENCIES
python -m pip install -r requirements.txt

3. CONFIGURE ENVIRONMENT VARIABLES
Create a .env file with the following values:

NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password


NEO4J SETUP
-----------
- Install Neo4j Desktop
- Enable Graph Data Science (GDS) plugin
- Load graph data using:

python graph/load_neo4j.py

Create graph projection (run once in Neo4j Browser):

CALL gds.graph.project(
  'movieGraph',
  ['Movie','Actor','Genre','Director'],
  {
    ACTED_IN:{type:'ACTED_IN',orientation:'UNDIRECTED'},
    HAS_GENRE:{type:'HAS_GENRE',orientation:'UNDIRECTED'},
    DIRECTED_BY:{type:'DIRECTED_BY',orientation:'UNDIRECTED'}
  }
);


RUN RECOMMENDATIONS
-------------------
python app.py

Example output:
Movie Title   | Final Score
---------------------------
Movie A       | 0.92
Movie B       | 0.89
Movie C       | 0.86


EVALUATION (OPTIONAL)
--------------------
- Precision@K
- NDCG@K
- hitFlop label used for offline evaluation


KEY LEARNINGS
-------------
- Embeddings capture semantic similarity between movies
- Graph algorithms capture structural importance and relationships
- Hybrid systems outperform single-method recommenders
- Neo4j enables explainable and cold-start friendly recommendations


FUTURE ENHANCEMENTS
-------------------
- Node Similarity (Jaccard / Cosine)
- User-based collaborative filtering
- RAG-based natural language explanations
- REST API (FastAPI / Spring Boot)
- Dashboard and visualization


AUTHOR
------
Built as a learning and portfolio project to explore recommendation systems,
graph databases, and hybrid machine learning architectures.
