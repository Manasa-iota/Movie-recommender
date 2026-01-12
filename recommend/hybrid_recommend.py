import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from graph.neo4j_utils import get_pagerank_candidates

df=pd.read_pickle("data/movies_with_embeddings.pkl")

def hybrid_recommend(imdbId,k=5):
    if imdbId not in df.imdbId.values:
        raise ValueError("Movie not found")

  
    target=df.loc[df.imdbId==imdbId,"embedding"].values[0]

   
    graph_results=get_pagerank_candidates(imdbId)

    if not graph_results:
        return []

    cand_ids,pageranks=zip(*graph_results)

    cand_df=df[df.imdbId.isin(cand_ids)].copy()
    cand_df["pagerank"]=cand_df.imdbId.map(
        dict(graph_results)
    )


    sims=cosine_similarity(
        [target],
        np.vstack(cand_df["embedding"].values)
    )[0]

    cand_df["cosine"]=sims


    cand_df["final_score"]=(
        0.7*cand_df["cosine"]
      + 0.3*cand_df["pagerank"]
    )

    
    cand_df=cand_df[cand_df.imdbId!=imdbId]

    return cand_df.sort_values(
        "final_score",ascending=False
    ).head(k)
