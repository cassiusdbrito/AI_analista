from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions() #não funciona com wb driver, talvez precise ser o caminho do pcs
options.add_argument("--start-maximized")  
driver = webdriver.Chrome(options=options)  

driver.get("https://chat.openai.com/")

time.sleep(5)

pergunta = "Me forneça 20 referências de sites sobre analise de dados com python"

for char in pergunta:
    webdriver.ActionChains(driver).send_keys(char).perform()
    time.sleep(0.05)  

webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()

time.sleep(60)

input("Pressione Enter para fechar o navegador...")
driver.quit()