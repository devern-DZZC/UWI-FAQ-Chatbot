import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.docstore.in_memory import InMemoryDocstore
from pprint import pprint
from dotenv import load_dotenv

from faiss import IndexFlatL2

load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

embedder = OpenAIEmbeddings(model='text-embedding-3-small', openai_api_key=OPEN_AI_API_KEY)

# 1. Define text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", ";", ",", " "]
)

print('Loading Documents...')

# 2. Load and flatten documents
docs = []
file_paths = [
    "undergrad_booklets/EngUndergrad.pdf",
    "undergrad_booklets/FoodAgriUndergrad.pdf",
    "undergrad_booklets/HumanitiesUndergrad.pdf",
    "undergrad_booklets/LawUndergrad.pdf",
    "undergrad_booklets/MedicalSciencesUndergrad.pdf",
    "undergrad_booklets/ScienceTechUndergrad.pdf",
    "undergrad_booklets/SocsciUndergrad.pdf",
    "undergrad_booklets/SportUndergrad.pdf",
    "undergrad_booklets/IGDS.pdf",
    "undergrad_booklets/UWI_FAQ.pdf"
]

info_map = {
    "EngUndergrad.pdf": {
        "title": "Faculty of Engineering Undergraduate Handbook",
        "faculty": "Engineering",
        "abbreviation": "FOE"
    },
    "FoodAgriUndergrad.pdf": {
        "title": "Faculty of Food & Agriculture Handbook",
        "faculty": "Food & Agriculture",
        "abbreviation": "FFA"
    },
    "HumanitiesUndergrad.pdf": {
        "title": "Faculty of Humanities and Education Handbook",
        "faculty": "Humanities and Education",
        "abbreviation": "FHE"
    },
    "LawUndergrad.pdf": {
        "title": "Faculty of Law Handbook",
        "faculty": "Law",
        "abbreviation": "LLB"
    },
    "MedicalSciencesUndergrad.pdf": {
        "title": "Faculty of Medical Sciences Handbook",
        "faculty": "Medical Sciences",
        "abbreviation": "FMS"
    },
    "ScienceTechUndergrad.pdf": {
        "title": "Faculty of Science and Technology Handbook",
        "faculty": "Science and Technology",
        "abbreviation": "FST"
    },
    "SocsciUndergrad.pdf": {
        "title": "Faculty of Social Sciences Handbook",
        "faculty": "Social Sciences",
        "abbreviation": "FSS"
    },
    "SportUndergrad.pdf": {
        "title": "Faculty of Sport Handbook",
        "faculty": "Sport",
        "abbreviation": "FSP"
    },
    "IGDS.pdf": {
        "title": "Institute for Gender and Development Studies Handbook",
        "faculty": "Gender and Development Studies",
        "abbreviation": "IGDS"
    },
    "UWI_FAQ.pdf": {
        "title": "University of the West Indies FAQ Document",
        "faculty": "General",
        "abbreviation": "UWI"
    }
}


for path in file_paths:
    docs.extend(PyPDFLoader(path).load())

print("Chunking documents...")

# 3. Split all documents into chunks
docs_chunks = text_splitter.split_documents(docs)

# 4. Enrich metadata and prepare document summary
doc_string = "Available Documents"
doc_metadata = []
essential_keys = ['source', 'page', 'title', 'total_pages', 'faculty', 'abbreviation']

seen_sources = set()

for i, chunk in enumerate(docs_chunks):
    metadata = getattr(chunk, 'metadata', {})
    source = metadata.get('source', 'Unknown')
    filename = source.split('/')[-1]

    # Enrich metadata from info_map if available
    extra_info = info_map.get(filename, {})
    chunk.metadata.update(extra_info)

    # Filter metadata keys
    chunk.metadata = {k: v for k, v in chunk.metadata.items() if k in essential_keys}

    chunk.metadata["chunk_index"] = i

    # Build doc_string summary using titles (avoid duplicates)
    if source not in seen_sources:
        title = chunk.metadata.get('title', source)
        doc_string += "\n - " + str(title)
        doc_metadata.append(str(chunk.metadata))
        seen_sources.add(source)

# 5. Combine for inspection or embedding
extra_chunks = [doc_string] + doc_metadata

print("\n--- Summary ---")
pprint(doc_string)

print("\n--- Sample Chunks ---")
print(f"Total chunks: {len(docs_chunks)}")
if docs_chunks:
    print("Example chunk metadata:")
    pprint(docs_chunks[9].metadata)
    print("Example content snippet:")
    print(docs_chunks[9].page_content[:300], "...")

print('\n\nConstructing Vector Store...')
vectorstore = FAISS.from_documents(docs_chunks, embedder)

## Sample Chunk Retrieval
query = "What courses do I have to take in Level 2 Semester 1. I am doing Computer Science Special"
query_embedding = embedder.embed_query(query)

# Get top k results with similarity score
results_with_scores = vectorstore.similarity_search_with_score_by_vector(query_embedding, k=5)

chunk_dict = vectorstore.docstore._dict
combined_chunks = []

for i, (doc, score) in enumerate(results_with_scores):
    base_index = doc.metadata.get("chunk_index")
    
    # Set lookahead based on rank
    if i < 2:
        current_lookahead = 4
    else:
        current_lookahead = 2
    
    combined_text = doc.page_content
    
    for offset in range(1, current_lookahead + 1):
        next_index = base_index + offset
        next_doc = chunk_dict.get(str(next_index))  # assuming keys are stringified ints
        
        if next_doc and next_doc.metadata.get("source") == doc.metadata.get("source"):
            combined_text += "\n\n" + next_doc.page_content
        else:
            break  # stop if source changes or chunk missing
    
    combined_chunks.append((combined_text, score, doc.metadata))

combined_chunks.sort(key=lambda x: x[1])


print(f"Constructed docstore with {len(vectorstore.docstore._dict)} chunks")

for i, (text, score, metadata) in enumerate(combined_chunks):
    print(f"\n--- Result {i+1} ---")
    print("Score:", score)
    print("Metadata:", metadata)
    print(text[:800], "..." if len(text) > 800 else "")


print("\n--- FULL COMBINED TEXT SENT TO GPT ---\n")
print(combined_chunks[0][0])


"""
# Uncomment to save Vector Store in this directory

print("\n\nSaving Vector Store...")
folder = "faiss_store"
os.makedirs(folder, exist_ok=True)
vectorstore.save_local(os.path.join(folder, "uwi_faq_faiss_index"))
print("Vector Store Saved!\n\n")

"""