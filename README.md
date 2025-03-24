# Assistente de Análise de Dados (Open Source)

Um assistente de análise de dados baseado em IA usando modelos open source do Hugging Face.

## Modelos Utilizados

- **Modelo de Linguagem**: BLOOM-560M (bigscience/bloom-560m)
- **Modelo de Embeddings**: all-MiniLM-L6-v2 (sentence-transformers)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/ai-analistadados.git
cd ai-analistadados
```

2. Instale as dependências usando Poetry:
```bash
poetry install
```

3. Configure as variáveis de ambiente:
- Crie um arquivo `.env` na raiz do projeto com as seguintes configurações:
```
# Configurações dos modelos
MODEL_NAME=bigscience/bloom-560m
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Configurações de processamento
MAX_LENGTH=512
TEMPERATURE=0.7
TOP_P=0.95

# Configurações de hardware
USE_CUDA=true
LOW_CPU_MEMORY=true
```

## Uso

```python
from ai_analistadados.models.assistente import AssistenteAnaliseDados

# Inicializa o assistente
assistente = AssistenteAnaliseDados()

# Faz uma pergunta
pergunta = "Como faço uma análise exploratória básica de um dataset usando pandas?"
resposta = assistente.processar_pergunta(pergunta)
print(resposta)

# Calcula similaridade semântica entre textos
texto1 = "Análise de dados com pandas"
texto2 = "Explorando datasets usando o pandas"
similaridade = assistente.similaridade_semantica(texto1, texto2)
print(f"Similaridade: {similaridade:.2f}")

# Limpa o histórico se necessário
assistente.limpar_memoria()
```

## Funcionalidades

- Análise exploratória de dados
- Visualização de dados
- Insights estatísticos
- Histórico de conversas
- Cálculo de similaridade semântica
- Suporte a CPU e GPU (CUDA)
- 100% Open Source

## Requisitos de Hardware

- CPU: Mínimo de 8GB de RAM recomendado
- GPU: Opcional, mas recomendado para melhor performance (CUDA compatível)

## Contribuindo

Contribuições são bem-vindas! Por favor, sinta-se à vontade para enviar um Pull Request.



