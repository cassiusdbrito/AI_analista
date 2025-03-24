from typing import List, Optional
import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class LangChainTrainer:
    def __init__(self):
        """
        Inicializa o treinador com modelos open source.
        Usa o modelo flan-t5-small para geração de texto e o all-MiniLM-L6-v2 para embeddings.
        """
        # Inicializar modelo de linguagem
        self.llm = HuggingFaceEndpoint(
            endpoint_url=os.getenv("HUGGINGFACE_ENDPOINT_URL", "https://api-inference.huggingface.co/models/google/flan-t5-small"),
            huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_TOKEN"),
            model_kwargs={
                "temperature": float(os.getenv("TEMPERATURE", 0.7)),
                "max_length": int(os.getenv("MAX_LENGTH", 512)),
                "top_p": float(os.getenv("TOP_P", 0.95))
            }
        )
        
        # Inicializar modelo de embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        )
        
        # Inicializar vetorstore
        self.vector_store = None
        
        # Configurar text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
    
    def carregar_dados_treinamento(self, diretorio: str):
        """
        Carrega dados de treinamento de arquivos .txt no diretório especificado.
        
        Args:
            diretorio: Caminho do diretório contendo os arquivos de treinamento
        """
        try:
            # Listar todos os arquivos .txt no diretório
            arquivos = []
            for root, _, files in os.walk(diretorio):
                for file in files:
                    if file.endswith('.txt'):
                        arquivos.append(os.path.join(root, file))
            
            if not arquivos:
                print(f"Nenhum arquivo .txt encontrado em {diretorio}")
                return
            
            # Carregar e processar cada arquivo
            documentos = []
            for arquivo in arquivos:
                try:
                    loader = TextLoader(arquivo, encoding='utf-8')
                    documentos.extend(loader.load())
                except Exception as e:
                    print(f"Erro ao carregar arquivo {arquivo}: {str(e)}")
            
            if not documentos:
                print("Nenhum documento foi carregado com sucesso")
                return
            
            # Dividir documentos em chunks
            chunks = self.text_splitter.split_documents(documentos)
            
            # Criar vetorstore
            self.vector_store = FAISS.from_documents(chunks, self.embeddings)
            print(f"Vetorstore criado com sucesso com {len(chunks)} chunks")
            
        except Exception as e:
            print(f"Erro ao carregar dados de treinamento: {str(e)}")
    
    def treinar(self, pergunta: str) -> str:
        """
        Treina o modelo com uma pergunta específica.
        
        Args:
            pergunta: A pergunta para treinar o modelo
            
        Returns:
            str: A resposta gerada pelo modelo
        """
        if not self.vector_store:
            return "Erro: Vetorstore não inicializado. Execute carregar_dados_treinamento primeiro."
        
        try:
            # Criar chain de recuperação
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(),
                return_source_documents=True
            )
            
            # Gerar resposta
            resultado = qa_chain({"query": pergunta})
            return resultado['result']
            
        except Exception as e:
            return f"Erro durante o treinamento: {str(e)}"
    
    def salvar_vetorstore(self, caminho: str):
        """
        Salva o vetorstore em disco.
        
        Args:
            caminho: Caminho onde salvar o vetorstore
        """
        if self.vector_store:
            self.vector_store.save_local(caminho)
            print(f"Vetorstore salvo em {caminho}")
        else:
            print("Nenhum vetorstore para salvar")
    
    def carregar_vetorstore(self, caminho: str):
        """
        Carrega um vetorstore salvo.
        
        Args:
            caminho: Caminho do vetorstore salvo
        """
        if os.path.exists(caminho):
            self.vector_store = FAISS.load_local(caminho, self.embeddings)
            print(f"Vetorstore carregado de {caminho}")
        else:
            print(f"Vetorstore não encontrado em {caminho}") 