from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.memory import InMemoryMemoryService
from google.adk.sessions import Session
from google.adk.tools import FunctionTool
from .tools import query_vectorstore
from dotenv import load_dotenv
load_dotenv()

session_service=InMemoryMemoryService()

APP_NAME="agents"
USER_ID="user-1"
SESSION_ID="session-1"

session=Session(
    app_name=APP_NAME,
    user_id=USER_ID,
    id=SESSION_ID
)

root_agent = Agent(
    name="workflow_agent",
    model="gemini-2.5-flash",
    static_instruction="You are a workflow writing agent with access to 'query_vectorstore' tool." \
    "For the task given by the user, invoke the tool to get 5 relevant workflows and using those workflows" \
    "as reference create a workflow to solve the given task." \
    "======[[INSTRUCTIONS]]======" \
    "1. Use only the model present in the workflows." \
    "2. Do not change the goddamn structure and logic of the workflows." \
    "3. Model details in the api-nodes should be kept as it is.",
    description="Workflow writing agent for segmind.",
    tools=[FunctionTool(query_vectorstore)],
)


runner=Runner(
    app_name=APP_NAME,
    session_service=session,
    agent=root_agent,
)
