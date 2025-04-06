import json
import os
import pandas as pd
import random

def carregar_dados(arquivo_json):
    """Carrega os dados do arquivo JSON"""
    with open(arquivo_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def formatar_para_llm(dados):
    """Formata os dados para treinamento de modelos de linguagem"""
    exemplos_formatados = []
    
    for item in dados:
        pergunta = item.get("pergunta", "")
        contexto = item.get("contexto", "")
        resposta = item.get("resposta", "")
        codigo = item.get("codigo", [])
        categoria = item.get("categoria", "")
        
        # Formata o exemplo para o modelo
        prompt = f"Pergunta: {pergunta}\n"
        
        if contexto:
            prompt += f"Contexto: {contexto}\n"
        
        prompt += "Resposta: "
        
        # Formata a resposta com código
        resposta_formatada = resposta
        if codigo:
            resposta_formatada += "\n\nCódigo:\n"
            for i, c in enumerate(codigo):
                resposta_formatada += f"```python\n{c}\n```\n"
        
        exemplos_formatados.append({
            "prompt": prompt,
            "completion": resposta_formatada,
            "categoria": categoria
        })
    
    return exemplos_formatados

def formatar_para_fine_tuning(dados, formato="jsonl"):
    """Formata os dados para fine-tuning de modelos"""
    if formato == "jsonl":
        # Formato para OpenAI, Anthropic, etc.
        exemplos = []
        
        for item in dados:
            pergunta = item.get("pergunta", "")
            contexto = item.get("contexto", "")
            resposta = item.get("resposta", "")
            codigo = item.get("codigo", [])
            
            # Formata o exemplo
            prompt = f"Pergunta: {pergunta}\n"
            
            if contexto:
                prompt += f"Contexto: {contexto}\n"
            
            prompt += "Resposta: "
            
            # Formata a resposta com código
            resposta_formatada = resposta
            if codigo:
                resposta_formatada += "\n\nCódigo:\n"
                for i, c in enumerate(codigo):
                    resposta_formatada += f"```python\n{c}\n```\n"
            
            exemplos.append({
                "prompt": prompt,
                "completion": resposta_formatada
            })
        
        return exemplos
    
    elif formato == "alpaca":
        # Formato para Alpaca, LLaMA, etc.
        exemplos = []
        
        for item in dados:
            pergunta = item.get("pergunta", "")
            contexto = item.get("contexto", "")
            resposta = item.get("resposta", "")
            codigo = item.get("codigo", [])
            
            # Formata o exemplo
            instrucao = f"Pergunta: {pergunta}\n"
            
            if contexto:
                instrucao += f"Contexto: {contexto}\n"
            
            # Formata a resposta com código
            resposta_formatada = resposta
            if codigo:
                resposta_formatada += "\n\nCódigo:\n"
                for i, c in enumerate(codigo):
                    resposta_formatada += f"```python\n{c}\n```\n"
            
            exemplos.append({
                "instruction": instrucao,
                "input": "",
                "output": resposta_formatada
            })
        
        return exemplos

def salvar_dados(dados, arquivo_saida, formato="json"):
    """Salva os dados no formato especificado"""
    if formato == "json":
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    
    elif formato == "jsonl":
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            for item in dados:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    elif formato == "csv":
        df = pd.DataFrame(dados)
        df.to_csv(arquivo_saida, index=False)

def dividir_dados(dados, proporcao_treino=0.8, proporcao_validacao=0.1):
    """Divide os dados em conjuntos de treino, validação e teste"""
    # Embaralha os dados
    random.shuffle(dados)
    
    # Calcula os índices de divisão
    n = len(dados)
    n_treino = int(n * proporcao_treino)
    n_validacao = int(n * proporcao_validacao)
    
    # Divide os dados
    treino = dados[:n_treino]
    validacao = dados[n_treino:n_treino+n_validacao]
    teste = dados[n_treino+n_validacao:]
    
    return treino, validacao, teste

def main():
    # Carrega os dados processados
    arquivo_entrada = "dados_treinamento/stackoverflow_qa_processado.json"
    dados = carregar_dados(arquivo_entrada)
    
    # Formata os dados para treinamento
    dados_formatados = formatar_para_llm(dados)
    
    # Divide os dados em conjuntos de treino, validação e teste
    treino, validacao, teste = dividir_dados(dados_formatados)
    
    # Salva os dados formatados
    diretorio_saida = "dados_treinamento/formatados"
    os.makedirs(diretorio_saida, exist_ok=True)
    
    # Salva no formato JSON
    salvar_dados(treino, f"{diretorio_saida}/treino.json")
    salvar_dados(validacao, f"{diretorio_saida}/validacao.json")
    salvar_dados(teste, f"{diretorio_saida}/teste.json")
    
    # Salva no formato JSONL para fine-tuning
    dados_fine_tuning = formatar_para_fine_tuning(dados, formato="jsonl")
    salvar_dados(dados_fine_tuning, f"{diretorio_saida}/fine_tuning.jsonl", formato="jsonl")
    
    # Salva no formato Alpaca
    dados_alpaca = formatar_para_fine_tuning(dados, formato="alpaca")
    salvar_dados(dados_alpaca, f"{diretorio_saida}/alpaca.json", formato="json")
    
    print(f"Concluído! Dados formatados salvos em {diretorio_saida}")
    print(f"Treino: {len(treino)} exemplos")
    print(f"Validação: {len(validacao)} exemplos")
    print(f"Teste: {len(teste)} exemplos")

if __name__ == "__main__":
    main() 