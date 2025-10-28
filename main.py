from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from prompt import MASTER_PROMPT
from langchain_community.vectorstores import FAISS
import os


OPENAI_API_KEY = ""

query=input("enter request: ")

embeddings_dir = os.path.join(os.path.dirname(__file__), "embeddings")
db = FAISS.load_local(embeddings_dir,embeddings=OpenAIEmbeddings(api_key=OPENAI_API_KEY,model="text-embedding-3-large"),allow_dangerous_deserialization=True)
res=db.similarity_search(query,k=5)

t=[]

for doc in res:
    t.append(doc.metadata['template'])

prompt=MASTER_PROMPT.format(
    temp1=t[0],
    temp2=t[1],
    temp3=t[2],
    temp4=t[3],
    temp5=t[4],
)

llm=ChatOpenAI(model="o3",api_key=OPENAI_API_KEY)
output = llm.invoke(prompt)

print(output)