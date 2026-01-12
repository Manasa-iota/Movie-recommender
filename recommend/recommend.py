import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

df=pd.read_pickle("data/movies_with_embeddings.pkl")

def recommend(imdbId,k=5):
    if imdbId not in df.imdbId.values:
        raise ValueError("Movie not found")

    target=df.loc[df.imdbId==imdbId,"embedding"].values[0]

    embeddings=np.vstack(df["embedding"].values)
    sims=cosine_similarity([target],embeddings)[0]

    results=df.copy()
    results["score"]=sims

    results=results[results.imdbId!=imdbId]

    return results.sort_values("score",ascending=False).head(k)

print(recommend("tt1234567"))
