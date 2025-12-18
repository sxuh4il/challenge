from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from app.config import config

def get_rag_chain(retriever):
    if not config.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set.")

    llm = ChatGoogleGenerativeAI(
        model=config.LLM_MODEL,
        google_api_key=config.GOOGLE_API_KEY,
        temperature=0.0
    )

    prompt_template = """You are an expert assistant for a Question-Answering task.

Instructions:
1. Answer the question based ONLY on the provided context below.
2. If the answer is not in the context, strictly reply: "I don't have enough information to answer this question based on the provided documents."
3. Do not invent information.
4. Answer in the SAME LANGUAGE as the question (e.g., if the question is in French, answer in French).

Context:
{context}

Question: {question}

Answer:"""

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": PROMPT
        }
    )

    return qa_chain