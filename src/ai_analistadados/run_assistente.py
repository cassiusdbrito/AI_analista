from ai_analistadados.models.assistente import AssistenteAnaliseDados
import os

def main():

    # Obter o caminho absoluto do diretório de dados
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    diretorio_dados = os.path.join(diretorio_atual, "dados_treinamento")
    
    # Exemplo de uso
    assistente = AssistenteAnaliseDados(diretorio_dados=diretorio_dados)
    
    # Exemplo de pergunta
    pergunta = input("Barra de pergunta: ")
    resposta = assistente.processar_pergunta(pergunta)
    print(f"Resposta: {resposta}")
    
    # Exemplo de similaridade semântica
    # texto1 = "Análise de dados com pandas"
    # texto2 = "Explorando datasets usando o pandas"
    # similaridade = assistente.similaridade_semantica(texto1, texto2)
    # print(f"Similaridade: {similaridade:.2f}")

if __name__ == "__main__":
    main() 