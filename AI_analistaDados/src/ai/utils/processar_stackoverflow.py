import os
import json
import pandas as pd
from bs4 import BeautifulSoup
import re

def limpar_texto(texto):
    """Remove tags HTML e limpa o texto"""
    if not texto:
        return ""
    
    # Remove tags HTML
    soup = BeautifulSoup(texto, 'html.parser')
    texto = soup.get_text()
    
    # Remove espaços extras
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto

def extrair_codigo(texto):
    """Extrai blocos de código do texto"""
    padrao_codigo = r'```(?:python)?\s*([\s\S]*?)```'
    codigos = re.findall(padrao_codigo, texto)
    
    if not codigos:
        # Tenta outro padrão comum
        padrao_codigo = r'<pre><code>([\s\S]*?)</code></pre>'
        codigos = re.findall(padrao_codigo, texto)
    
    return codigos

def processar_arquivo(arquivo):
    """Processa um arquivo do StackOverflow para extrair pergunta e resposta"""
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Limpa o conteúdo
    texto_limpo = limpar_texto(conteudo)
    
    # Divide em linhas
    linhas = texto_limpo.split('\n')
    
    # Procura por padrões de pergunta
    pergunta = ""
    contexto = ""
    resposta = ""
    codigo = []
    
    # Procura por títulos de pergunta
    for i, linha in enumerate(linhas):
        if linha.strip() and not pergunta:
            pergunta = linha.strip()
            # Pega algumas linhas após a pergunta como contexto
            contexto = '\n'.join(linhas[i+1:i+5])
            break
    
    # Procura por respostas
    for i, linha in enumerate(linhas):
        if "Answer" in linha or "Resposta" in linha or "Solution" in linha or "Solução" in linha:
            # Pega o conteúdo após a palavra-chave
            resposta = '\n'.join(linhas[i+1:i+20])
            break
    
    # Se não encontrou resposta específica, tenta pegar o restante do conteúdo
    if not resposta and pergunta:
        # Pega o conteúdo após a pergunta
        inicio_resposta = texto_limpo.find(pergunta) + len(pergunta)
        resposta = texto_limpo[inicio_resposta:].strip()
    
    # Extrai código da resposta
    codigo = extrair_codigo(resposta)
    
    # Remove o código da resposta para deixar apenas o texto explicativo
    for c in codigo:
        resposta = resposta.replace(c, "")
    
    # Limpa a resposta novamente
    resposta = limpar_texto(resposta)
    
    return {
        "pergunta": pergunta,
        "contexto": contexto,
        "resposta": resposta,
        "codigo": codigo
    }

def processar_diretorio(diretorio):
    """Processa todos os arquivos em um diretório"""
    resultados = []
    
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.txt'):
            caminho_completo = os.path.join(diretorio, arquivo)
            categoria = os.path.basename(diretorio)
            
            try:
                qa = processar_arquivo(caminho_completo)
                if qa["pergunta"] and (qa["resposta"] or qa["codigo"]):
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
    arquivo_saida = "dados_treinamento/stackoverflow_qa_processado.json"
    
    resultados = []
    
    # Processa cada subdiretório
    for categoria in os.listdir(diretorio_base):
        caminho_categoria = os.path.join(diretorio_base, categoria)
        if os.path.isdir(caminho_categoria):
            print(f"Processando categoria: {categoria}")
            qa_categoria = processar_diretorio(caminho_categoria)
            resultados.extend(qa_categoria)
    
    print(f"Salvando {len(resultados)} pares de pergunta-resposta...")
    salvar_resultados(resultados, arquivo_saida)
    
    print(f"Concluído! Arquivo salvo em {arquivo_saida}")

if __name__ == "__main__":
    main() 