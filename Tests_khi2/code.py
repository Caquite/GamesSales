import pandas as pd
import numpy as np

a_cat = pd.read_csv("gamesale_table_a_categorie.csv")
a_os = pd.read_csv("gamesale_table_a_os.csv")
a_tag = pd.read_csv("gamesale_table_a_tag.csv")
cat = pd.read_csv("gamesale_table_categorie.csv")
dev = pd.read_csv("gamesale_table_developpeur.csv")
editeur = pd.read_csv("gamesale_table_editeur.csv")
genre = pd.read_csv("gamesale_table_genre.csv")
jeux = pd.read_csv("gamesale_table_jeux.csv")
os = pd.read_csv("gamesale_table_os.csv")

df = pd.merge(jeux,dev)
df = pd.merge(df,editeur)
df = pd.merge(df,genre)
print(df.head())