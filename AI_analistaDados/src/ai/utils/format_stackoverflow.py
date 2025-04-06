import os
import re
import json
from bs4 import BeautifulSoup
import pandas as pd

def limpar_html(texto):
    """Remove tags HTML e limpa o texto"""
    soup = BeautifulSoup(texto, 'html.parser')
    return soup.get_text().strip()

def extrair_pergunta_resposta(arquivo):
    """Extrai pergunta e resposta de um arquivo do StackOverflow"""
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Limpa o conteúdo
    conteudo = limpar_html(conteudo)
    
    # Tenta identificar pergunta e resposta
    # Padrão comum: título da pergunta seguido de conteúdo
    linhas = conteudo.split('\n')
    
    # Procura por padrões de pergunta
    pergunta = ""
    resposta = ""
    
    # Procura por títulos de pergunta
    for i, linha in enumerate(linhas):
        if linha.strip() and not pergunta:
            pergunta = linha.strip()
            # Pega algumas linhas após a pergunta como contexto
            contexto = '\n'.join(linhas[i+1:i+5])
            break
    
    # Procura por respostas (geralmente após a pergunta)
    for i, linha in enumerate(linhas):
        if "Answer" in linha or "Resposta" in linha or "Solution" in linha or "Solução" in linha:
            # Pega o conteúdo após a palavra-chave
            resposta = '\n'.join(linhas[i+1:i+20])
            break
    
    # Se não encontrou resposta específica, tenta pegar o restante do conteúdo
    if not resposta and pergunta:
        # Pega o conteúdo após a pergunta
        inicio_resposta = conteudo.find(pergunta) + len(pergunta)
        resposta = conteudo[inicio_resposta:].strip()
    
    return {
        "pergunta": pergunta,
        "contexto": contexto if 'contexto' in locals() else "",
        "resposta": resposta
    }

def formatar_arquivos(diretorio_base):
    """Formata todos os arquivos em um diretório"""
    resultados = []
    
    # Percorre todos os subdiretórios
    for raiz, dirs, arquivos in os.walk(diretorio_base):
        for arquivo in arquivos:
            if arquivo.endswith('.txt'):
                caminho_completo = os.path.join(raiz, arquivo)
                categoria = os.path.basename(raiz)
                
                try:
                    qa = extrair_pergunta_resposta(caminho_completo)
                    if qa["pergunta"] and qa["resposta"]:
                        qa["categoria"] = categoria
                        qa["arquivo"] = arquivo
                        resultados.append(qa)
                except Exception as e:
                    print(f"Erro ao processar {caminho_completo}: {e}")
    
    return resultados

def salvar_resultados(resultados, arquivo_saida):
    """Salva os resultados em formato JSON"""
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    
    # Também salva em CSV para fácil visualização
    df = pd.DataFrame(resultados)
    df.to_csv(arquivo_saida.replace('.json', '.csv'), index=False)

def main():
    diretorio_base = "dados_treinamento/exemplos/stackoverflow"
    arquivo_saida = "dados_treinamento/stackoverflow_qa.json"
    
    print(f"Formatando arquivos de {diretorio_base}...")
    resultados = formatar_arquivos(diretorio_base)
    
    print(f"Salvando {len(resultados)} pares de pergunta-resposta...")
    salvar_resultados(resultados, arquivo_saida)
    
    print(f"Concluído! Arquivo salvo em {arquivo_saida}")

if __name__ == "__main__":
    main() 