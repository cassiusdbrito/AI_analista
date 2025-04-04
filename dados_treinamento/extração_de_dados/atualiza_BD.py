from wscrap_docs import extrair_exemplos_documentacao
from extrac_notebooks import extrair_codigos_notebooks
from extrac_github import extrair_exemplos_github
import os
from dotenv import load_dotenv
# from monitoramento import monitorar_novos_conteudos

load_dotenv()

def main():
    # Criar diretórios necessários
    os.makedirs('dados_treinamento/exemplos/extraidos', exist_ok=True)
    os.makedirs('dados_treinamento/exemplos/notebooks', exist_ok=True)
    os.makedirs('dados_treinamento/exemplos/github', exist_ok=True)
    
    # Executar extrações
    extrair_exemplos_documentacao()
    extrair_codigos_notebooks()
    extrair_exemplos_github()
    
    # Iniciar monitoramento
    # monitorar_novos_conteudos()

if __name__ == "__main__":
    main()