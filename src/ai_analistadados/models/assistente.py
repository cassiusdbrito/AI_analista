from typing import List, Optional
import os
from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceEndpoint
from langchain.memory import ConversationBufferMemory
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from ai_analistadados.models.langchain_trainer import LangChainTrainer
import torch

load_dotenv()

class AssistenteAnaliseDados:
    def __init__(self, diretorio_dados: Optional[str] = None):
        """
        Inicializa o assistente de análise de dados usando LangChain e modelos open source.
        Usa o modelo Llama para geração de código e o all-MiniLM-L6-v2 para embeddings.
        
        Args:
            diretorio_dados: Diretório opcional contendo dados de treinamento
        """
        # Verificar token da API
        api_token = os.getenv("HUGGINGFACE_API_TOKEN")
        if not api_token:
            raise ValueError(
                "Token da API do Hugging Face não encontrado. "
                "Por favor, configure a variável de ambiente HUGGINGFACE_API_TOKEN "
                "no arquivo .env com seu token válido."
            )
        
        # Configurar dispositivo (CPU/GPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Inicializar modelo de linguagem via LangChain
        print("Carregando modelo de linguagem...")
        try:
            self.llm = HuggingFaceEndpoint(
                endpoint_url=os.getenv("HUGGINGFACE_ENDPOINT_URL", "https://api-inference.huggingface.co/models/codellama/CodeLlama-7b-hf"),
                huggingfacehub_api_token=api_token,
                task="text-generation",
                model_kwargs={
                    "temperature": float(os.getenv("TEMPERATURE", 0.1)),
                    "max_length": int(os.getenv("MAX_LENGTH", 256)),
                    "top_p": float(os.getenv("TOP_P", 0.95)),
                    "device": self.device,
                    "max_new_tokens": 256,  # Reduzido para 256
                    "return_full_text": False,
                    "do_sample": True,
                    "num_return_sequences": 1,
                    "repetition_penalty": 1.2,
                    "stop": ["```", "Human:", "Assistant:"]  # Tokens de parada
                }
            )
        except Exception as e:
            raise ValueError(
                f"Erro ao inicializar o modelo do Hugging Face: {str(e)}\n"
                "Verifique se seu token é válido e se você tem acesso ao modelo."
            )
        
        # Inicializar memória de conversação
        self.memory = ConversationBufferMemory(
            memory_key="history",
            return_messages=True,
            input_key="input"
        )
        
        # Inicializar modelo de embeddings
        print("Carregando modelo de embeddings...")
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
            )
        except Exception as e:
            raise ValueError(
                f"Erro ao inicializar o modelo de embeddings: {str(e)}\n"
                "Verifique se você tem acesso ao modelo de embeddings."
            )
        
        # Inicializar vetorstore
        self.vectorstore = FAISS.from_texts(
            ["Análise de dados com pandas", "Visualização de dados com matplotlib"],
            self.embeddings
        )
        
        # Inicializar trainer se diretório de dados for fornecido
        self.trainer = None
        if diretorio_dados:
            print("Carregando dados de treinamento...")
            self.trainer = LangChainTrainer()
            self.trainer.carregar_dados_treinamento(diretorio_dados)
    
    def processar_pergunta(self, pergunta: str) -> str:
        """
        Processa uma pergunta do usuário e retorna uma resposta.
        
        Args:
            pergunta: A pergunta do usuário sobre análise de dados.
            
        Returns:
            str: A resposta do assistente.
        """
        try:
            # Buscar contexto relevante se trainer estiver disponível
            contexto = ""
            if self.trainer and self.trainer.vector_store:
                docs = self.trainer.vector_store.similarity_search(pergunta, k=1)
                contexto = docs[0].page_content if docs else ""
            
            # Carregar histórico da conversa
            historico = self.memory.load_memory_variables({})['history']
            
            # Preparar prompt com contexto (mais conciso)
            prompt_completo = f"""<s>[INST] Gere código Python para:
            {pergunta}
            
            Use pandas e matplotlib.
            Comente em português.
            [/INST]</s>
            
            Resposta:"""
            
            # Processar pergunta usando o modelo
            try:
                # Usar invoke em vez de predict
                resposta = self.llm.invoke(prompt_completo)
                if not resposta or resposta.strip() == "":
                    raise ValueError("Resposta vazia recebida do modelo")
                
                # Limpar resposta de possíveis repetições
                resposta = resposta.strip()
                linhas = resposta.split('\n')
                linhas_unicas = []
                for linha in linhas:
                    if linha not in linhas_unicas:
                        linhas_unicas.append(linha)
                resposta = '\n'.join(linhas_unicas)
                
                # Atualizar memória
                self.memory.save_context({"input": pergunta}, {"output": resposta})
                return resposta
            except Exception as e:
                print(f"Erro ao gerar resposta: {str(e)}")
                raise
            
        except Exception as e:
            print(f"Erro detalhado: {str(e)}")
            return f"Desculpe, ocorreu um erro ao processar sua pergunta. Por favor, tente novamente ou reformule sua pergunta."
    
    def limpar_memoria(self):
        """
        Limpa o histórico de conversas.
        """
        self.memory.clear()
    
    def similaridade_semantica(self, texto1: str, texto2: str) -> float:
        """
        Calcula a similaridade semântica entre dois textos.
        
        Args:
            texto1: Primeiro texto
            texto2: Segundo texto
            
        Returns:
            float: Score de similaridade entre 0 e 1
        """
        # Calcular embeddings
        embedding1 = self.embeddings.embed_query(texto1)
        embedding2 = self.embeddings.embed_query(texto2)
        
        # Calcular similaridade de cosseno
        similarity = torch.nn.functional.cosine_similarity(
            torch.tensor(embedding1).unsqueeze(0),
            torch.tensor(embedding2).unsqueeze(0)
        )
        
        return similarity.item() 