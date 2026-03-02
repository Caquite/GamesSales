# Quantitative vs Qualitative Analysis (Boîte à moustaches)

This file contains the Python logic for generating **Boxplots**. It compares a numerical variable (like Sales or Price) against a categorical variable (like Genre or Editor).

## Key Features
* **Auto-Cleaning:** Automatically converts text decimals (e.g., "12,5") to Python numbers.
* **Outlier Removal:** Filters out the top 1% of extreme values (like "Wii Sports" sales) so the graph remains readable.
* **Timeline Protection:** Automatically detects "Years" and disables the outlier filter so we don't accidentally delete "old" games.

## The Python Code

```python
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

def getBDD():
    try:
        return mysql.connector.connect(
            host='localhost', database='gamesale',
            user='root', password='', charset='utf8'
        )
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

RELATIONSHIPS = {
    'genre': "JOIN genre ON jeux.id_jeu = genre.id_jeu",
    'editeur': "JOIN editeur ON jeux.id_jeu = editeur.id_jeu",
    'developpeur': "JOIN developpeur ON jeux.id_jeu = developpeur.id_jeu",
    'os': "JOIN a_os ON jeux.id_jeu = a_os.id_jeu JOIN os ON a_os.id_os = os.id_os",
    'categorie': "JOIN a_categorie ON jeux.id_jeu = a_categorie.id_jeu JOIN categorie ON a_categorie.id_cat = categorie.id_cat"
}

def plot_boxplot_relationship(col_x, table_x, col_y, table_y):
    connect = getBDD()
    if not connect: return

    # 1. SQL JOIN LOGIC (Multi-join support)
    needed_joins = set()
    if table_x != 'jeux' and table_x in RELATIONSHIPS:
        needed_joins.add(RELATIONSHIPS[table_x])
    if table_y != 'jeux' and table_y in RELATIONSHIPS:
        needed_joins.add(RELATIONSHIPS[table_y])
    
    sql_from = f"jeux {' '.join(needed_joins)}"
    sql = f"SELECT {table_x}.{col_x}, {table_y}.{col_y} FROM {sql_from}"
    
    print(f"🚀 Executing Boxplot SQL: {sql}")
    df = pd.read_sql(sql, connect)
    connect.close()

    # 2. FORCE NUMERIC CONVERSION
    # We detect which one should be the number (usually Annee, Prix, or Ventes)
    num_col = None
    cat_col = None

    for col in [col_x, col_y]:
        if any(k in col.lower() for k in ['annee', 'prix', 'ventes']):
            num_col = col
        else:
            cat_col = col

    # If we couldn't find a "named" number, we guess based on data type
    if not num_col:
        num_col = col_y if df[col_y].dtype != 'object' else col_x
        cat_col = col_x if num_col == col_y else col_y

    df[num_col] = df[num_col].astype(str).str.replace(',', '.')
    df[num_col] = pd.to_numeric(df[num_col], errors='coerce')
    df = df.dropna(subset=[num_col])

    # 3. Apply the < 70 filter (but ONLY for Sales or Price, not Years!)
    if 'annee' not in num_col.lower():
        upper_limit = df[num_col].quantile(0.90)
        df = df[df[num_col] <= upper_limit]

    # 3. THE BOXPLOT
    plt.figure(figsize=(14, 8))
    
    # Sort categories by the median of the numeric column for a cleaner look
    order = df.groupby(cat_col)[num_col].median().sort_values(ascending=False).index
    
    # showfliers=True shows the outliers (the dots)
    sns.boxplot(data=df, x=cat_col, y=num_col, order=order, palette='viridis')

    # --- INTEGER FIX (For Years) ---
    if 'annee' in num_col.lower():
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    plt.title(f'Distribution of {num_col} by {cat_col}', fontsize=15)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Example Test: 
plot_boxplot_relationship('genre', 'genre', 'prix', 'jeux')
```