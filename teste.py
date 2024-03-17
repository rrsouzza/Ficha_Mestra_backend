"""# Site para conferir o JSON --> https://jsonlint.com/ */

import json

Todos_arquivos = {}

with open("dicionario_RPG.json", encoding='utf-8') as arquivos:
    dados = json.load(arquivos)

for i in dados:
    Todos_arquivos.update(i)

print(Todos_arquivos["Classes"].keys())"""



teste =[]
print(len(teste))