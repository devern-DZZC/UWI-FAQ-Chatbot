from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.schema.document import Document
from pprint import pprint

# 1. Define text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
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

for chunk in docs_chunks:
    metadata = getattr(chunk, 'metadata', {})
    source = metadata.get('source', 'Unknown')
    filename = source.split('/')[-1]

    # Enrich metadata from info_map if available
    extra_info = info_map.get(filename, {})
    chunk.metadata.update(extra_info)

    # Filter metadata keys
    chunk.metadata = {k: v for k, v in chunk.metadata.items() if k in essential_keys}

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
    pprint(docs_chunks[0].metadata)
    print("Example content snippet:")
    print(docs_chunks[0].page_content[:300], "...")
