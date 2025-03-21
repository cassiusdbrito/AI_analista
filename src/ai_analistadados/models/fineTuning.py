
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Carregar o modelo CodeLlama (ou outro modelo de geração de código)
MODEL_NAME = "codellama/CodeLlama-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, device_map="auto")

def gerar_codigo(pergunta):
    prompt = f"### Pergunta:\n{pergunta}\n\n### Código:\n"
    
    # Tokenizar a entrada
    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")

    # Gerar a resposta
    output = model.generate(**inputs, max_length=100, temperature=0.3, do_sample=True)


    # Decodificar a saída
    codigo_gerado = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Remover o prompt da resposta final
    return codigo_gerado.replace(prompt, "").strip()

# Exemplo de uso
def main():
    pergunta = input("Digite sua pergunta: ")
    codigo = gerar_codigo(pergunta)
    print("\nCódigo Gerado:\n")
    print(codigo)

main()
