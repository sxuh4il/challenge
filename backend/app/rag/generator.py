from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.config import config

def get_rag_chain(retriever):
    if not config.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set.")

    llm = ChatGoogleGenerativeAI(
        model=config.LLM_MODEL,
        google_api_key=config.GOOGLE_API_KEY,
        temperature=0.0
    )

    prompt = PromptTemplate(
        template="""You are an expert assistant for a Question-Answering task.

Instructions:
1. Answer the question based ONLY on the provided context below.
2. If the answer is not in the context, strictly reply:
   "I don't have enough information to answer this question based on the provided documents."
3. Do not invent information.
4. Answer in the SAME LANGUAGE as the question.

Context:
{context}

Question: {question}

Answer:""",
        input_variables=["context", "question"]
    )

    llm_chain = LLMChain(llm=llm, prompt=prompt)

    def rag_chain(inputs: dict):
        docs = retriever.get_relevant_documents(inputs["question"])
        context = "\n\n".join(doc.page_content for doc in docs)

        result = llm_chain.invoke({
            "context": context,
            "question": inputs["question"]
        })

        return {
            "result": result["text"],
            "source_documents": docs
        }

    return rag_chain
