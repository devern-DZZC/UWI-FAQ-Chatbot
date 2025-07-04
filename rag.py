import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.schema.runnable import RunnableLambda
from langchain.schema.runnable.passthrough import RunnableAssign
from langchain_community.document_transformers import LongContextReorder
from langchain_community.docstore.in_memory import InMemoryDocstore
from faiss import IndexFlatL2


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from functools import partial
from operator import itemgetter
from pprint import pprint

from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")

instruct_llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)
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

embed_dims = len(embedder.embed_query("test"))
def default_FAISS():
    return FAISS(
        embedding_function=embedder,
        index=IndexFlatL2(embed_dims),
        docstore=InMemoryDocstore(),
        index_to_docstore_id= {},
        normalize_L2=False
    )

def save_memory_and_get_output(d, vstore):
    vstore.add_texts([
        f"User previously responded with {d.get('input')}",
        f"Agent previously responded with {d.get('output')}"
    ])
    return d.get('output')

long_reorder = RunnableLambda(LongContextReorder().transform_documents)

# Load the vector store
print('Loading Vectorstore...')
docstore = FAISS.load_local("faiss_store/uwi_faq_faiss_index", embeddings=embedder, allow_dangerous_deserialization=True)
print('Vectorstore Loaded!')

# Create chat prompt
chat_prompt = ChatPromptTemplate.from_messages([("system",
        "You are a document chatbot. Help the user as they ask questions about the documents."
        "User messaged just asked: {input}\n\n"
        "Conversation History Retrieval:\n{history}\n\n"
        "Document Retrieval:\n{context}\n\n"
        "(Answer only from retrieval. Make your responses conversational. If you do not know a response,"
        "tell the user to contact Student Administration. Do not ask follow up questions)"),
        ('user', '{input}')])

convstore = default_FAISS()

stream_chain = chat_prompt | instruct_llm | StrOutputParser()

# Retrieve relevant chunks
retrieval_chain = (
    {'input': (lambda x:x)}
    | RunnableAssign({'history': itemgetter('input') | convstore.as_retriever(search_kwargs={'k':5}) | long_reorder | doc2str})
    | RunnableAssign({'context': itemgetter('input') | docstore.as_retriever(search_kwargs={'k':5}) | long_reorder | doc2str})
)

def chat_gen(message, history=[], return_buffer=True):
    buffer = ""
    retrieval = retrieval_chain.invoke(message)
    line_buffer = ""

    for token in stream_chain.stream(retrieval):
        buffer += token
        yield buffer if return_buffer else token
    
    save_memory_and_get_output({'input': message, 'output': buffer}, convstore)


MAX_QUESTIONS = 3
for i in range(MAX_QUESTIONS):
    user_input = input(f"\n\nQuestion {i+1}/{MAX_QUESTIONS}: ")
    print("\nAnswer:")
    full_response = ""
    for response in chat_gen(user_input, return_buffer=True):
        full_response = response

    print(full_response)
