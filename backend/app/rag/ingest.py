import os
import glob
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.config import config

def load_documents() -> List[Document]:
    documents = []
    
    # Supported extensions
    pdf_files = glob.glob(os.path.join(config.DATA_PATH, "*.pdf"))
    txt_files = glob.glob(os.path.join(config.DATA_PATH, "*.txt"))
    md_files = glob.glob(os.path.join(config.DATA_PATH, "*.md"))
    
    all_files = pdf_files + txt_files + md_files
    
    print(f"Found {len(all_files)} documents in {config.DATA_PATH}")

    for file_path in all_files:
        try:
            if file_path.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            elif file_path.endswith(".txt"):
                loader = TextLoader(file_path)
            elif file_path.endswith(".md"):
                loader = UnstructuredMarkdownLoader(file_path)
            else:
                continue
                
            documents.extend(loader.load())
            print(f"Loaded: {file_path}")
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            
    return documents

def ingest_docs():
    docs = load_documents()
    if not docs:
        print("No documents found to ingest.")
        return

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP
    )
    
    chunks = text_splitter.split_documents(docs)
    print(f"Created {len(chunks)} chunks.")

    print(f"Loading embedding model: {config.EMBEDDING_MODEL}")
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)

    print("Creating vector store...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    print(f"Saving vector store to {config.VECTOR_DB_PATH}")
    vectorstore.save_local(config.VECTOR_DB_PATH)
    print("Ingestion complete.")

if __name__ == "__main__":
    ingest_docs()
