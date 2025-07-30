import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")
VECTORSTORE_PATH = "faiss_store/uwi_faq_faiss_index"