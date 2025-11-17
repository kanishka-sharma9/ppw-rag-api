from langchain_community.vectorstores import FAISS
import os
from langchain_openai.embeddings import OpenAIEmbeddings

OPENAI_API_KEY = "sk-proj-**"

def query_vectorstore(query:str) -> list[dict]:
    """Tool for querying the vectorstore and returning
    data in """

    db = FAISS.load_local("C:\\Users\kanis\\Segmind\\ppw-rag\\embeddings",embeddings=OpenAIEmbeddings(api_key=OPENAI_API_KEY,model="text-embedding-3-large"),allow_dangerous_deserialization=True)

    docs = db.similarity_search(query,k=5)
    
    pretty_docs = []
    for doc in docs:
        pair={
            'title': doc.page_content,
            'template': doc.metadata['template']
        }

        pretty_docs.append(pair)

    return pretty_docs

def file_read():
    """ Tool for extracting file contents of 'models.json'"""
    models=None
    with open('models.json','r',encoding='utf-8') as f:
        models=json.load(f)

    return models

# if __name__=="__main__":
#     print(file_read())
