from fastapi import FastAPI
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
import os
import logging
import json
from datetime import datetime
from langchain_community.vectorstores import FAISS
from prompt import MASTER_PROMPT

# Get API key from environment variable or use hardcoded fallback
OPENAI_API_KEY = ""

# Create logs directory
logs_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(logs_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(logs_dir, "api.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Request counter
request_counter = 0

app=FastAPI()

llm = ChatOpenAI(model='gpt-5',api_key=OPENAI_API_KEY,temperature=0.8)

embeddings_dir = os.path.join(os.path.dirname(__file__), "embeddings")
db = FAISS.load_local(embeddings_dir,embeddings=OpenAIEmbeddings(api_key=OPENAI_API_KEY,model="text-embedding-3-large"),allow_dangerous_deserialization=True)

@app.post('/generate_workflow')
def generate_workflow(request:str):
    global request_counter
    request_counter += 1
    current_count = request_counter

    logger.info(f"Request #{current_count}: Received query: {request}")

    t=[]
    res=db.similarity_search(request,k=5)

    # Log retrieved documents to a numbered file
    log_file_path = os.path.join(logs_dir, f"request_{current_count:04d}.json")
    log_data = {
        "request_number": current_count,
        "timestamp": datetime.now().isoformat(),
        "query": request,
        "retrieved_documents": []
    }

    for idx, doc in enumerate(res, 1):
        print(doc.metadata['template'])
        t.append(doc.metadata['template'])

        # Add to log data
        log_data["retrieved_documents"].append({
            "rank": idx,
            "page_content": doc.page_content,
            "metadata_keys": list(doc.metadata.keys())
        })

        logger.info(f"Request #{current_count} - Doc {idx}: {doc.page_content[:100]}...")

    # Save detailed log to file
    with open(log_file_path, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

    logger.info(f"Request #{current_count}: Retrieved documents saved to {log_file_path}")

    prompt=MASTER_PROMPT.format(
        temp1=t[0],
        temp2=t[1],
        temp3=t[2],
        temp4=t[3],
        temp5=t[4],
    )

    # print(prompt)
    output=llm.invoke(prompt)

    logger.info(f"Request #{current_count}: Workflow generation complete")

    return output.content