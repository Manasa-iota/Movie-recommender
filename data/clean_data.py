import pandas as pd

df=pd.read_csv('data/Movies.csv')

df=df.drop_duplicates(subset=["imdbId"])
df["actors"]=df["actors"].fillna("")
df["genre"]=df["genre"].fillna("")
df["directors"]=df["directors"].fillna("")


df["actor_list"]=df["actors"].apply(lambda x:x.split(","))
df["genre_list"]=df["genre"].apply(lambda x:x.split(","))
df.to_pickle("data/clean_movies.pkl")