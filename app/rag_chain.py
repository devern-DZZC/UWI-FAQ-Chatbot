from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable.passthrough import RunnableAssign
from operator import itemgetter

from app.config import OPENAI_API_KEY, VECTORSTORE_PATH
from app.retriever import embedder, doc2str, long_reorder, default_FAISS
from langchain_community.vectorstores import FAISS

# Load vectorstore
docstore = FAISS.load_local(VECTORSTORE_PATH, embeddings=embedder, allow_dangerous_deserialization=True)
convstore = default_FAISS()

# Model
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)

# Prompt
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a document chatbot. Help the user as they ask questions about the documents."
     "User messaged just asked: {input}\n\n"
     "Conversation History Retrieval:\n{history}\n\n"
     "Document Retrieval:\n{context}\n\n"
     "(Answer only from retrieval. Make your responses conversational. "
     "If you do not know a response, tell the user to contact Student Administration. "
     "Do not ask follow up questions)"),
    ("user", "{input}")
])

# Stream chain
stream_chain = chat_prompt | llm | StrOutputParser()

# Retrieval logic
retrieval_chain = (
    {'input': (lambda x: x)}
    | RunnableAssign({'history': itemgetter('input') | convstore.as_retriever(search_kwargs={'k': 5}) | long_reorder | doc2str})
    | RunnableAssign({'context': itemgetter('input') | docstore.as_retriever(search_kwargs={'k': 5}) | long_reorder | doc2str})
)

# Main generator
def chat_response(message: str):
    buffer = ""
    retrieval = retrieval_chain.invoke(message)

    for token in stream_chain.stream(retrieval):
        buffer += token

    # Optionally save conv to memory
    convstore.add_texts([
        f"User previously responded with {message}",
        f"Agent previously responded with {buffer}"
    ])

    return buffer
