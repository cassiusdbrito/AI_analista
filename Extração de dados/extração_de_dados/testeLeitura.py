# Abrindo o arquivo e lendo as linhas
#import os
#print("Diretório atual:", os.getcwd())
with open("Extração de dados/extração_de_dados/perguntas.txt", "r", encoding="utf-8") as arquivo:
    linhas = [linha.strip() for linha in arquivo]

print(linhas)
