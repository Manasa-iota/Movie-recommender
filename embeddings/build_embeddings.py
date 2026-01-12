import pandas as pd
import torch
from transformers import AutoTokenizer,AutoModel

df=pd.read_pickle("data/clean_movies.pkl")

tokenizer=AutoTokenizer.from_pretrained("ai4bharat/indic-bert")
model=AutoModel.from_pretrained("ai4bharat/indic-bert")

def embed(row):
    text=f"{row.title} {row.genre} {row.actors} {row.directors}"
    inputs=tokenizer(text,return_tensors="pt",padding=True,truncation=True)
    with torch.no_grad():
        out=model(**inputs)
    return out.last_hidden_state.mean(dim=1).squeeze().numpy()

df["embedding"]=df.apply(embed,axis=1)
df.to_pickle("data/movies_with_embeddings.pkl")
