from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import Agent 
from google.adk.models.lite_llm import LiteLlm
from google.adk.a2a.utils.agent_to_a2a import to_a2a  
# to_a2a는 우리가 만든 이 agent를 받아서 몇거ㅏ지를 바꿀수도잇고 아닐수도있을
# 우리가 만든 agent를 읽고 이 정보들을 사용해서 agent를 노출하는 server 생성

# dummy tool 생성 
def dummy_tool(hello:str):
    """Dummy Tool. Helos the agent"""
    return "world"

agent = Agent(
    name = "HistoryHelperAgent",
    description="An agent that can help  students with history homework",
    model = LiteLlm("openai/gpt-4o"),
    tools = [dummy_tool],
    sub_agents=[]
)

app = to_a2a(agent, port = 8001) # 서버를 만들어줌 

