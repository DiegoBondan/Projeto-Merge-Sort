import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv
import time

inicio = time.time()

load_dotenv()

HOST     = os.getenv("HOST")
PORT     = os.getenv("PORT")
DBNAME   = os.getenv("DBNAME")
USER     = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

conn = psycopg2.connect(
    host=HOST,
    port=PORT,
    dbname=DBNAME,
    user=USER,
    password=PASSWORD
)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS dados_ordenados (
        id INTEGER,
        nome VARCHAR(100),
        valor NUMERIC
    )
""")

df_final = pd.read_csv("dados_200k_ordenados.csv")

dados = list(df_final[["id", "nome", "valor"]].itertuples(index=False, name=None))
execute_values(cursor, "INSERT INTO dados_ordenados (id, nome, valor) VALUES %s", dados)

conn.commit()
cursor.close()
conn.close()
print(f"Tempo de inserção: {time.time() - inicio:.2f} segundos")
print("Dados inseridos com sucesso no banco!")