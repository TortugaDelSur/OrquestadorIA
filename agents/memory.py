import os
import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

class AgentMemory:
    def __init__(self):
        # Directorio donde se guardará la base de datos de vectores
        self.persist_directory = "./data/chroma_db"
        
        # Usamos OpenAI para convertir texto en números (embeddings)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
        # Inicializamos la base de datos Chroma
        self.vector_db = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name="sales_reports"
        )

    def save_analysis(self, text, metadata):
        """Guarda el análisis de la IA en la base de datos vectorial."""
        try:
            self.vector_db.add_texts(texts=[text], metadatas=[metadata])
            print("Análisis guardado con éxito en la memoria.")
        except Exception as e:
            print(f"Error al guardar en memoria: {e}")

    def search_past_reports(self, query, k=2):
        """Busca fragmentos de análisis anteriores que se parezcan a la consulta."""
        try:
            results = self.vector_db.similarity_search(query, k=k)
            return "\n---\n".join([res.page_content for res in results])
        except Exception as e:
            print(f"No se pudo recuperar memoria: {e}")
            return ""