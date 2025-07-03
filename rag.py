import os, pprint
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import FAISS
from langchain.schema.runnable import RunnableLambda
from langchain.schema.runnable.passthrough import RunnableAssign
from langchain.document_transformers import LongContextReorder


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from functools import partial

from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")

instruct_llm = OpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)
embedder = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)


## Utility Functions to make life easier
def RPrint(preface=""):
    def print_and_return(x, preface):
        if preface: print(preface, end="")
        pprint(x)
        return x
    return RunnableLambda(partial(print_and_return, preface=preface))

def doc2str(docs, title=""):
    out_str = ""
    for doc in docs:
        doc_name = getattr(doc, 'metadata', {}).get('Title', title)
        if doc_name:
            out_str += f"[Quote from {doc_name}]"
        out_str += getattr(doc, 'page_content', str(doc)) + "\n"
    return out_str

long_reorder = RunnableLambda(LongContextReorder().transform_documents)

# Load the vector store
print('Loading Vectorstore...')
docstore = FAISS.load_local("faiss_store/uwi_faq_faiss_index", embeddings=embedder, allow_dangerous_deserialization=True)
print('Vectorstore Loaded!')

# Create chat prompt
chat_prompt = ChatPromptTemplate.from_messages([("system",
        "You are a dcoument chatbot. Help the user as they ask questions about the documents."
        "User messaged just asked: {input}\n\n"
        "Conversation History Retrieval:\n{history}\n\n"
        "Document Retrieval:\n{context}\n\n"
        "(Answer only from retrieval. Make your responses conversational. If you do not know a response,"
        "tell the user to contact Student Administration and provide their contact)"),
        ('user', '{input}')])

stream_chain = chat_prompt | RPrint() | instruct_llm | StrOutputParser()

# Retrieve relevant chunks
retrieval_chain = (
    {
        'context': docstore.as_retriever() | long_reorder | doc2str,
        'input': (lambda x:x)
    }
    | RunnableAssign({'output': chat_prompt | instruct_llm | StrOutputParser()})
)

