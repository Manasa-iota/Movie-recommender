#  Hybrid Movie Recommendation System (Graph + Embeddings)

A hybrid movie recommendation system that combines **semantic similarity using transformer-based embeddings**
with **graph-based ranking using Neo4j Personalized PageRank** to deliver accurate, explainable,
and cold-start friendly recommendations.

---

##   Features

- Content-based recommendations using **Indic-BERT embeddings**
- Relationship-aware recommendations using **Neo4j graph database**
- **Personalized PageRank** for graph-based ranking (Neo4j GDS)
- Hybrid scoring combining graph importance and cosine similarity
- Cold-start support (no user history required)
- Modular and extensible architecture

---

##  System Architecture

```
Movie Metadata
      |
      v
Text Embeddings (Indic-BERT)
      |
      v
Cosine Similarity --------\
                            ---> Hybrid Ranking ---> Top-K Recommendations
Neo4j Graph ---> PageRank-/
```

---

##  Dataset

Each movie record contains the following fields:

- imdbId
- title
- releaseYear
- releaseDate
- genre
- writers
- actors
- directors
- sequel
- hitFlop

**Text used for embeddings:**

```
title + genre + actors + directors
```

---

##  Recommendation Strategy

### 1️ Content-Based Filtering

- Movies are encoded into dense vectors using **Indic-BERT**
- Similarity between movies is computed using **cosine similarity**

### 2️ Graph-Based Recommendation (Neo4j)

Movies are modeled as a heterogeneous graph:

```
(Movie) --ACTED_IN--> (Actor)
(Movie) --HAS_GENRE--> (Genre)
(Movie) --DIRECTED_BY--> (Director)
(Movie) --SEQUEL_OF--> (Movie)
```

### 3️ Graph Algorithm

- **Personalized PageRank** using Neo4j Graph Data Science
- Ranks movies based on structural importance relative to a given movie

### 4️ Hybrid Ranking

Final score calculation:

```
FinalScore =
  0.7 * CosineSimilarity
+ 0.3 * PageRankScore
```

---

##  Project Structure

```
movie-recommender/
├── data/
│   ├── movies.csv
│   ├── clean_movies.pkl
│   └── movies_with_embeddings.pkl
│
├── embeddings/
│   └── build_embeddings.py
│
├── graph/
│   ├── load_neo4j.py
│   └── neo4j_utils.py
│
├── recommend/
│   ├── recommend.py
│   └── hybrid_recommend.py
│
├── eval/
│   └── metrics.py
│
├── app.py
├── requirements.txt
├── .env
└── README.md
```

---

##  Setup Instructions

###  Create Virtual Environment

```bash
python -m venv venv
```

Activate:

- **Windows**
  ```bash
  venv\Scripts\activate
  ```

- **Linux / Mac**
  ```bash
  source venv/bin/activate
  ```

---

###  Install Dependencies

```bash
python -m pip install -r requirements.txt
```

---

###  Configure Environment Variables

Create a `.env` file in the project root:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
```

---

## Neo4j Setup

- Install **Neo4j Desktop**
- Enable **Graph Data Science (GDS)** plugin
- Load graph data:

```bash
python graph/load_neo4j.py
```

Create graph projection (run once in Neo4j Browser):

```cypher
CALL gds.graph.project(
  'movieGraph',
  ['Movie','Actor','Genre','Director'],
  {
    ACTED_IN:    {type:'ACTED_IN',    orientation:'UNDIRECTED'},
    HAS_GENRE:   {type:'HAS_GENRE',   orientation:'UNDIRECTED'},
    DIRECTED_BY:{type:'DIRECTED_BY', orientation:'UNDIRECTED'}
  }
);
```

---

## Run Recommendations

```bash
python app.py
```

Example output:

```
Movie Title        Final Score
-----------------------------
Movie A            0.92
Movie B            0.89
Movie C            0.86
```

---

## Evaluation 

- Precision@K
- NDCG@K
- hitFlop label used for offline evaluation

---


