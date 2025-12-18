from app.rag.retriever import get_retriever
from app.rag.generator import get_rag_chain
import logging

logging.basicConfig(level=logging.INFO)

def main():
    print("\n🚀 Starting RAG standalone test...\n")

    retriever = get_retriever()
    print("✅ Retriever loaded")

    chain = get_rag_chain(retriever)
    print("✅ RAG chain loaded")

    question = "What is this document about?"
    print(f"\n❓ Question: {question}\n")

    # ✅ Utilisation dynamique de la clé d'entrée
    input_key = list(chain.input_keys)[0]
    print("Using input key:", input_key)

    response = chain.invoke({input_key: question})

    print("🧠 Answer:\n")
    print(response["result"])

    print("\n📚 Sources:\n")
    for doc in response["source_documents"]:
        print("-", doc.metadata.get("source", "unknown"))

    print("\n✅ RAG test finished successfully")


if __name__ == "__main__":
    main()
