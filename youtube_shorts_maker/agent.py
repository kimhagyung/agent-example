from google.adk.agents import Agent 
from google.adk.models.lite_llm import LiteLlm 
from google.adk.tools.agent_tool import AgentTool
from .sub_agents.content_planner.agent import content_planner_agent
from .sub_agents.asset_generator.agent import asset_generator_agent
from .sub_agents.video_assembler.agent import video_assembler_agent
from .prompt import SHORTS_PRODUCER_DESCRIPTION, SHORTS_PRODUCER_PROMPT

MODEL = LiteLlm(model="openai/gpt-4o")
# content_planner  가 결정적으로 영상메이커 이기 때문에 지금 openai/gpt-4o 이 모델 말고 더 비싼 모델을 사용해도됨 

shorts_producer_agent = Agent(
    name = "ShortsProducerAgent",
    model = MODEL,
    description=SHORTS_PRODUCER_DESCRIPTION , 
    instruction=SHORTS_PRODUCER_PROMPT,
    tools=[
        AgentTool(agent=content_planner_agent),
        AgentTool(agent=asset_generator_agent),
        AgentTool(agent=video_assembler_agent),
    ]
)

root_agent = shorts_producer_agent