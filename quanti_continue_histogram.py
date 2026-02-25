import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def getBDD():
    try:
        bdd = mysql.connector.connect(
            host='localhost',
            database='gamesale',
            user='root',
            password='',
            charset='utf8'
        )
        return bdd
    except Exception as e:
        print("Connection Error: " + str(e))
        return None

def graph_quanti_continue(column_name):
    #Histogram !
    connect = getBDD()
    sql = f"SELECT {column_name} FROM jeux"
    df = pd.read_sql(sql, connect)
    connect.close()

    df[column_name] = df[column_name].astype(str).str.replace(',', '.')
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
    df = df.dropna(subset=[column_name])

    plt.figure(figsize=(10, 5))
    sns.histplot(data=df, x=column_name, kde=True, color='skyblue')
    plt.title(f'Histogram of {column_name}')
    plt.show()

#test
graph_quanti_continue('Ventes_Global')
#graph_quanti_continue('prix')