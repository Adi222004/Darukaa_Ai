import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DOCS_DIR = "data/documents"
VECTORSTORE_DIR = "data/vectorstore"

def load_documents():
    docs = []
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
        return docs
    for file in os.listdir(DOCS_DIR):
        path = os.path.join(DOCS_DIR, file)
        if file.endswith(".pdf"):
            docs.extend(PyPDFLoader(path).load())
        elif file.endswith(".txt"):
            docs.extend(TextLoader(path).load())
    return docs

def ingest():
    print("Loading documents...")
    documents = load_documents()
    if not documents:
        print("No documents found. Add files to data/documents/")
        return
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks. Generating embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=VECTORSTORE_DIR)
    db.persist()
    print(f"Successfully ingested {len(chunks)} chunks into the vector database.")

if __name__ == "__main__":
    ingest()