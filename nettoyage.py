import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

FILE_PATH = 'votre_fichier_final.csv'
CIBLE = 'Global_Sales'  #var cible pour la prediction hohoho

df = pd.read_csv(FILE_PATH)

#descriptions
print("Processing Descriptions...")
tfidf = TfidfVectorizer(stop_words='english', max_features=50) # Keep top 20 words only
text_matrix = tfidf.fit_transform(df['description_du_jeu'].fillna(''))

#dataframe pour les mots
df_text = pd.DataFrame(
    text_matrix.toarray(), 
    columns=[f"word_{w}" for w in tfidf.get_feature_names_out()]
)


#encodage des categories & publishers
print("Processing Categories...")

#encodage de top 30 publishers, le reste devient 'Other'
top_publishers = df['Publisher'].value_counts().nlargest(30).index
df['Publisher'] = df['Publisher'].apply(lambda x: x if x in top_publishers else 'Other')

#colonnes pour chaque catégorie et si fait partie de la catégorie c’est 1 et s’il n’en fait pas partie c 0
df_dummies = pd.get_dummies(df[['Genre', 'Publisher', 'Platform']], drop_first=True)


#Combination: Original Numerics + One-Hot Categories + TF-IDF Words
#We drop non-numeric columns
numeric_cols = df.select_dtypes(include=np.number).columns
X_numeric = df[numeric_cols].drop(columns=[CIBLE], errors='ignore')

#concatenation 
X = pd.concat([X_numeric, df_dummies, df_text], axis=1)
y = df[CIBLE] #la var cible

#tout vide vaut 0
X = X.fillna(0)
print(f"Final Dataset Shape: {X.shape} (Rows, Columns)")


# 688 Train / 344 Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# Scale (Crucial for KNN and Linear Regression interpretation)
scaler = StandardScaler()
# We convert back to DataFrame to keep column names + lisible
X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X.columns)
X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X.columns)