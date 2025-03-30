import requests
from bs4 import BeautifulSoup
from transformers import AutoModelForCausalLM, AutoTokenizer

print("inicio")

urls = [
    "https://www.datacamp.com/pt/tutorial/types-of-data-plots-and-how-to-create-them-in-python",
    "https://www.dio.me/articles/8-graficos-fundamentais-para-data-science-utilizando-python",
    "https://www.alura.com.br/artigos/matplotlib-python",
    "https://matplotlib.org/stable/contents.html"
]

def get_text_from_url(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all("p") 
        text = "\n".join([p.get_text() for p in paragraphs])
        return text
    else:
        print(f"Erro ao acessar {url}")
        return ""
collected_data = ""
for url in urls:
    collected_data += get_text_from_url(url) + "\n\n" 

#erro
model_name = "codellama/CodeLlama-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def feed_ai_with_data(data):
    inputs = tokenizer(collected_data, return_tensors="pt", truncation=True, max_length=4096).to("cpu")
    output = model.generate(**inputs, max_new_tokens=100)
    return tokenizer.decode(output[0], skip_special_tokens=True)

ai_response = feed_ai_with_data(collected_data)
print(ai_response) #sem retorno