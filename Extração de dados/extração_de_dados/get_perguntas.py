from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time


def salvar_titulos(titulo, caminho_arquivo):
    # Primeiro lê o conteúdo atual do arquivo
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            titulos_existentes = set(linha.strip().lower() for linha in f)
    except FileNotFoundError:
        # Se o arquivo não existe ainda, começa vazio
        titulos_existentes = set()

    titulo_formatado = titulo.strip().lower()
    
    with open(caminho_arquivo, 'a', encoding='utf-8') as f:
        if titulo not in titulos_existentes:
            f.write(titulo.strip() + '\n')


def pega_perguntas(URL, assuntos):
    driver = webdriver.Chrome()
    driver.get(URL)
    perguntas_filtradas = []

    try:
        # Loop principal
        while True:
            time.sleep(2)  # Pequena pausa pra garantir carregamento
            
            # Pega todas as perguntas
            perguntas = driver.find_elements(By.CSS_SELECTOR, '.s-post-summary')
            
            for pergunta in perguntas:
                try:
                    titulo_element = pergunta.find_element(By.CSS_SELECTOR, '.s-post-summary--content-title a')
                    titulo = titulo_element.text
                    link = titulo_element.get_attribute('href')
                    
                    if link and "questions" in link and any(assunto.lower() in titulo.lower() for assunto in assuntos):
                        perguntas_filtradas.append((titulo, link))
                        
                except Exception as e:
                    print(f"Erro ao processar pergunta: {e}")
            
            # Agora tenta encontrar botão "Next"
            try:
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[rel="next"]'))
                )
                print("Indo para próxima página...")
                next_button.click()
            except (TimeoutException, NoSuchElementException):
                print("Não achei botão 'Next'. Provavelmente acabou!")
                break  # Se não achou, acabou a navegação

    except KeyboardInterrupt:
        print("Parando web scraping manualmente...")
    
    finally:
        driver.quit()  # Fecha o navegador SEMPRE (mesmo em erro ou Ctrl+C)
        return perguntas_filtradas

def main():
    assuntos_desejados = ["pandas", "numpy", "matplolib", "data analyses", "seaborn", "ETL", "import csv",
                          "Machine Learning", "pytorch", "scikit-learn", "pre-process data"]
    
    url = 'https://stackoverflow.com/questions'

    perguntas = pega_perguntas(url, assuntos_desejados)

    print(f"\nTotal de perguntas capturadas: {len(perguntas)}\n")
    for titulo, link in perguntas:
        print(titulo)
        print(link)
        salvar_titulos(titulo, "Extração de dados/extração_de_dados/perguntas1.txt")
        print("-" * 50)

if __name__ == "__main__":
    main()

