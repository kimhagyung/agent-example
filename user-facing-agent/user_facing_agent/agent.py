from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import Agent 
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH
)

philosophy_agent = RemoteA2aAgent(
    name ="HistoryHelperAgent",
    description="An agent that can help  students with history homework", 
    agent_card = f"http://127.0.0.1:8001/{AGENT_CARD_WELL_KNOWN_PATH}" # agent card의 url 정해야함 
)

history_agent = RemoteA2aAgent(
    name ="PhilosophyHelperAgent",
    description="An agent that can help  students with Philosophy homework", 
    agent_card = f"http://127.0.0.1:8002/{AGENT_CARD_WELL_KNOWN_PATH}" # agent card의 url 정해야함 
)

root_agent = Agent(
    name = "StudentHelperAgent",
    description="An agent that can help students with their homework",
    model = LiteLlm("openai/gpt-4o"),
    sub_agents=[ # 나중에 adk로 만든 다른 port에서 실행될 romte agent가 들어감 
        history_agent
    ]
)