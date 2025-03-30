import requests
from bs4 import BeautifulSoup
import os

def buscar_stackoverflow_api(termo, num_resultados=5):
    print(f"Buscando perguntas sobre: {termo}")
    
    URL = f"https://api.stackexchange.com/2.3/search"
    params = {
        'order': 'desc',
        'sort': 'activity',
        'intitle': termo,
        'site': 'stackoverflow',
        'pagesize': num_resultados
    }
    resposta = requests.get(URL, params=params)
    
    if resposta.status_code != 200:
        print(f"Erro ao acessar a API: {resposta.status_code}")
        return []

    dados = resposta.json()

    # verificando as perguntas
    perguntas = dados.get('items', [])
    print(f"Encontradas {len(perguntas)} perguntas.")
    
    links = []
    for pergunta in perguntas:
        link = pergunta.get('link')
        if link:
            links.append(link)
    print(f"Links das perguntas: {links}")
    
    return links

def extrair_codigo_stackoverflow(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Captura os blocos de código em tags <pre>, <code>, etc.
    blocos_codigo = soup.find_all(['pre', 'code'])
    
    exemplos = []
    for bloco in blocos_codigo:
        texto = bloco.get_text()
        # Verifica se o código parece ser Python
        if "import " in texto or "def " in texto or "print(" in texto:
            exemplos.append(texto)

    return exemplos

def salvar_codigos_separados_stackoverflow(exemplos, termo):
    os.makedirs(f"dados_treinamento/exemplos/stackoverflow/{termo}", exist_ok=True)
    for i, exemplo in enumerate(exemplos):
        nome_arquivo = f"dados_treinamento/exemplos/extraidos/stackoverflow/{termo}/exemplo_{i}.txt"

        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write(exemplo)

def extracao_stackoverflow_api():
    #termos do chatgpt
    termos_de_busca = [
        "pandas tutorial",
        "scikit-learn example",
        "matplotlib plot",
        "numpy array",
        "tensorflow training loop",
        "pytorch example",
        "data analysis python",
        "python plotting example"
    ]
    
    for termo in termos_de_busca:
        print(f"\nIniciando busca para o termo: {termo}")
        urls = buscar_stackoverflow_api(termo)
        
        for url in urls:
            print(f"URL encontrada: {url}")
            exemplos = extrair_codigo_stackoverflow(url)
            if exemplos:
                salvar_codigos_separados_stackoverflow(exemplos, termo)


extracao_stackoverflow_api()
