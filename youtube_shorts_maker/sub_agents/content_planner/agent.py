from google.adk.agents import Agent 
from google.adk.models.lite_llm import LiteLlm 
from .prompt import CONTENT_PLANNER_DESCRIPTION, CONTENT_PLANNER_PROMPT 
from .models import ContentPlanOutput # model.py 
 
MODEL = LiteLlm(model="openai/gpt-4o")

content_planner_agent = Agent(
    name = "ContentPlannerAgent",
    description=CONTENT_PLANNER_DESCRIPTION,
    instruction=CONTENT_PLANNER_PROMPT,
    model = MODEL,
    output_schema=ContentPlanOutput, 
    output_key="content_planner_output",  #output_key에 뭐든 넣으면 그 이름으로 결과물이 state에 저장된다.  
)
