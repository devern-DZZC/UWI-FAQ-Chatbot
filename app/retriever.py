from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from faiss import IndexFlatL2
from app.config import OPENAI_API_KEY
from langchain_community.document_transformers import LongContextReorder
from langchain.schema.runnable import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain.schema.runnable.passthrough import RunnableAssign

embedder = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)

def doc2str(docs, title=""):
    out_str = ""
    for doc in docs:
        doc_name = getattr(doc, 'metadata', {}).get('Title', title)
        if doc_name:
            out_str += f"[Quote from {doc_name}]"
        out_str += getattr(doc, 'page_content', str(doc)) + "\n"
    return out_str

def default_FAISS():
    return FAISS(
        embedding_function=embedder,
        index=IndexFlatL2(len(embedder.embed_query("test"))),
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
        normalize_L2=False
    )

long_reorder = RunnableLambda(LongContextReorder().transform_documents)