from operator import itemgetter
import cohere
from typing import Dict, Any

from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable.passthrough import RunnableAssign
from langchain_community.vectorstores import FAISS

from app.config import VECTORSTORE_PATH, COHERE_API_KEY
from app.retriever import embedder, doc2str, long_reorder, default_FAISS

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

# Load vectorstores
docstore = FAISS.load_local(
    VECTORSTORE_PATH,
    embeddings=embedder,
    allow_dangerous_deserialization=True
)
convstore = default_FAISS()

# Prompt Template - modified to work with Cohere's API
def prepare_cohere_prompt(message: str, history: str, context: str) -> str:
    return (
        "You are an AI assistant trained to help users by answering questions based only on the retrieved documents. "
        "Rules:\n"
        "- Answer only using the content in the documents\n"
        "- If unsure, say 'I'm not sure based on the documents I have. Please contact Student Administration.'\n"
        "- Never invent information\n"
        "- Be concise and helpful\n\n"
        f"Conversation History:\n{history}\n\n"
        f"Document Context:\n{context}\n\n"
        f"User Question: {message}"
    )

# Retrieval chain (unchanged)
retrieval_chain = (
    {'input': (lambda x: x)}
    | RunnableAssign({
        'history': itemgetter('input') | convstore.as_retriever(search_kwargs={'k': 5}) | long_reorder | doc2str
    })
    | RunnableAssign({
        'context': itemgetter('input') | docstore.as_retriever(search_kwargs={'k': 5}) | long_reorder | doc2str
    })
)

def chat_response(message: str) -> str:
    # Get context and history
    retrieval = retrieval_chain.invoke(message)
    
    # Prepare the prompt
    prompt = prepare_cohere_prompt(
        message=message,
        history=retrieval['history'],
        context=retrieval['context']
    )
    
    # Call Cohere API
    response = co.chat(
        model="command-r-plus",
        message=prompt,
        temperature=0.3,
        max_tokens=1000,
        chat_history=[]  # You can populate this with previous messages if needed
    )
    
    # Store conversation
    convstore.add_texts([
        f"User: {message}",
        f"Agent: {response.text}"
    ])
    
    return response.text