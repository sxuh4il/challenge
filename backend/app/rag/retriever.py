import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import config

def get_retriever():
    if not os.path.exists(config.VECTOR_DB_PATH):
        raise FileNotFoundError(f"Vector store not found at {config.VECTOR_DB_PATH}. Run ingestion first.")
    
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
    
    # Allow dangerous deserialization since we trust our own local index file
    vectorstore = FAISS.load_local(config.VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    
    return vectorstore.as_retriever(search_kwargs={"k": config.RETRIEVAL_K})
