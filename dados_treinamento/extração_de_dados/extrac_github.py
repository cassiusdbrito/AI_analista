import requests
import os
from dotenv import load_dotenv

load_dotenv()

def extrair_exemplos_github():
    # Configuração da API do GitHub
    headers = {
        'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'
    }
    '''
    Tem que buscar mais diretórios pra repositórios relevantes

    '''
    # Buscar repositórios relevantes
    repos = [
        'pandas-dev/pandas',
        'scikit-learn/scikit-learn',
        'matplotlib/matplotlib'
    ]
    
    for repo in repos:
        # Buscar arquivos Python
        response = requests.get(f'https://api.github.com/repos/{repo}/contents/examples', headers=headers)
        arquivos = response.json()
        
        for arquivo in arquivos:
            if arquivo['name'].endswith('.py'):
                # Baixar conteúdo
                conteudo = requests.get(arquivo['download_url'], headers=headers).text
                
                # Salvar em arquivo
                with open(f'dados_treinamento/exemplos/github/{arquivo["name"]}.txt', 'w') as f:
                    f.write(conteudo)