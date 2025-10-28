from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document
from templates import LIST
import json
import os

# Get API key from environment variable or use hardcoded fallback
OPENAI_API_KEY = ""

print("Building docs...")
docs = []
for task_desc, temp in LIST:
    docs.append(
        Document(page_content=task_desc,metadata={"template":json.dumps(temp)})
    )
print("Doc building complete...")

print("indexing...")
db = FAISS.from_documents(documents=docs,embedding=OpenAIEmbeddings(api_key=OPENAI_API_KEY,model="text-embedding-3-large"))

# Create embeddings directory if it doesn't exist
embeddings_dir = os.path.join(os.path.dirname(__file__), "embeddings")
os.makedirs(embeddings_dir, exist_ok=True)

db.save_local(embeddings_dir)

print("indexing complete...")