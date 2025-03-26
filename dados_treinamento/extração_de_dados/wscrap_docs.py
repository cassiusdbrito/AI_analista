import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def extrair_exemplos_documentacao():
    # URLs de documentação relevante
    urls = [
        'https://pandas.pydata.org/docs/getting_started/',
        'https://scikit-learn.org/stable/tutorial/index.html',
        'https://matplotlib.org/tutorials/index.html'
    ]
    
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extrair exemplos de código
        exemplos = soup.find_all('pre')
        
        # Salvar exemplos em arquivos
        for i, exemplo in enumerate(exemplos):
            with open(f'dados_treinamento/exemplos/extraidos/exemplo_{i}.txt', 'w') as f:
                f.write(exemplo.text)