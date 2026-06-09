import pandas as pd
import heapq
import os
import time
inicio = time.time()

ARQUIVO_ENTRADA  = "dados_200k.csv"
TAMANHO_BLOCO    = 100_000
PASTA_TEMPORARIA = "temp_blocos"
COLUNA_ORDEM     = "id"

os.makedirs(PASTA_TEMPORARIA, exist_ok=True)

blocos = []

for i, chunk in enumerate(pd.read_csv(ARQUIVO_ENTRADA, chunksize=TAMANHO_BLOCO)):
    chunk.sort_values(by=COLUNA_ORDEM, inplace=True)
    nome_arquivo = f"{PASTA_TEMPORARIA}/bloco_{i}.csv"
    chunk.to_csv(nome_arquivo, index=False)
    blocos.append(nome_arquivo)

arquivos = [open(b, "r") for b in blocos]
headers  = [f.readline().strip() for f in arquivos]

def proxima(i):
    linha = arquivos[i].readline()
    if linha:
        valores = linha.strip().split(",")
        return (int(valores[0]), i, linha)
    return None

heap = []
for i in range(len(arquivos)):
    item = proxima(i)
    if item:
        heapq.heappush(heap, item)

with open("dados_200k_ordenados.csv", "w") as out:
    out.write(headers[0] + "\n")
    while heap:
        valor, i, linha = heapq.heappop(heap)
        out.write(linha)
        prox = proxima(i)
        if prox:
            heapq.heappush(heap, prox)
    for f in arquivos:
        f.close()
    for b in blocos:
        os.remove(b)

os.rmdir(PASTA_TEMPORARIA)
print(f"Tempo de ordenação: {time.time() - inicio:.2f} segundos")
print("Arquivo ordenado com sucesso!")
