import time
import pyautogui
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import firebase_admin


# Caminho do chromedriver
chromedriver_path = r"C:\Users\cassi\Desktop\chromedriver.exe"

cred = firebase_admin.credentials.Certificate("bbafc8210d3200073510143890ac3e137aa2e0db")
firebase_admin.initialize_app(cred)
db = firebase_admin.firestore.client()
# Perguntas
perguntas = [
    "Como eu faço um grafico de barras com python? Me responda no modelo [pergunta, resposta]",
]

# Lista de respostas
respostas = []

# Config do navegador
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Coordenadas da caixa de pergunta (ajuste conforme necessário)
caixa_pergunta = (640, 946)

# Loop principal
for pergunta in perguntas:
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
    driver.get("https://copilot.microsoft.com/")

    print(f"🔎 Enviando pergunta: {pergunta}")

    # Aguarda carregamento do site
    time.sleep(8)

    # Clica na caixa de entrada
    pyautogui.click(*caixa_pergunta)
    time.sleep(1)

    # Cola a pergunta
    pyperclip.copy(pergunta)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)

    # Envia
    pyautogui.press("enter")

    # Aguarda a resposta aparecer
    try:
        resposta_div = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'group') and contains(@class, 'ai-message-item')]"))
        )
        time.sleep(2)  # Pequena pausa extra para garantir o carregamento do texto
        resposta = resposta_div.text.strip()
    except TimeoutException:
        resposta = None

    respostas.append(resposta)

    driver.quit()
    time.sleep(3)

for i, r in enumerate(respostas):
    if r:
        pergunta = perguntas[i]
        print(f"🔹 Pergunta {i+1}: {pergunta}")
        print(f"🔸 Resposta:\n{r}\n{'-'*50}")

        # Salva no Firebase Firestore
        doc_ref = db.collection("perguntas_respostas").document()  # cria doc com ID automático
        doc_ref.set({
            "pergunta": pergunta,
            "resposta": r,
            "timestamp": firebase_admin.firestore.SERVER_TIMESTAMP
        })