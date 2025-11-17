from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.memory import InMemoryMemoryService
from google.adk.sessions import Session
from google.adk.tools import FunctionTool,AgentTool
from .tools import query_vectorstore,file_read
from dotenv import load_dotenv

load_dotenv()

session_service=InMemoryMemoryService()

APP_NAME="rag_agent"
USER_ID="user-1"
SESSION_ID="session-1"

session=Session(
    app_name=APP_NAME,
    user_id=USER_ID,
    id=SESSION_ID
)

planner_agent = Agent(
    name='Workflow_planner',
    model='gemini-2.5-flash',
    description="Workflow planning agent for segmind ",
    instruction="You are a helpful and experienced workflow planning assistant for segmind. " \
    "Your job is to understand and explore the possibilities of the given user query to" \
    "generate a highly detailed, step-by-step plan for a workflow (DAG). " \
    "The plan must include details about: " \
    "1. Input nodes " \
    "2. Model nodes and the prompts " \
    "3. Output nodes " \
    "4. structure and flow of the graph " \
    "5. final output " \
    "Add more details if needed, but do not deviate from the assigned task. ",
)

workflow_agent = Agent(
    name="Workflow_creator",
    model="gemini-2.5-flash",
    instruction="You are a workflow writing agent with access to 'query_vectorstore' and 'planner_agent' tools. " \
    "For the task given by the user, first generate a plan using 'planner_agent', then invoke the 'query_vectorstore' tool to get 5 relevant workflows and using those workflows " \
    "as reference create a workflow to solve the task. " \
    "======[[INSTRUCTIONS]]====== " \
    "1. Use only the model present in the workflows. " \
    "2. Do not change the structure and logic of the workflows. " \
    "3. Model details in the api-nodes should be kept as it is. " \
    "4. The prompts should be complete and detailed, without any placeholders. " \
    "5. Use the 'file_read' tool for searching through all available models in 'model.json' "
    "   and choosing the best model by comparing the description and model types with the given task",
    description="Workflow writing agent for segmind.",
    tools=[
        FunctionTool(query_vectorstore),
        AgentTool(planner_agent),
        FunctionTool(file_read)
    ],
)

root_agent=workflow_agent

runner=Runner(
    app_name=APP_NAME,
    session_service=session,
    agent=root_agent,
)
