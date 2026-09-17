from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

VECTORSTORE_DIR = "data/vectorstore"

def retrieve(query: str):
    if not os.path.exists(VECTORSTORE_DIR):
        return []
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma(persist_directory=VECTORSTORE_DIR, embedding_function=embeddings)
    
    # Retrieve top 3 chunks
    docs = vectordb.similarity_search(query, k=3)
    return [{"content": d.page_content, "metadata": d.metadata} for d in docs]