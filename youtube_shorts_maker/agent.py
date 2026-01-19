from google.genai import types
from google.adk.agents import Agent  
from google.adk.models.lite_llm import LiteLlm 
from google.adk.tools.agent_tool import AgentTool
from .sub_agents.content_planner.agent import content_planner_agent
from .sub_agents.asset_generator.agent import asset_generator_agent
from .sub_agents.video_assembler.agent import video_assembler_agent
from .prompt import SHORTS_PRODUCER_DESCRIPTION, SHORTS_PRODUCER_PROMPT
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse

MODEL = LiteLlm(model="openai/gpt-4o")
# content_planner  가 결정적으로 영상메이커 이기 때문에 지금 openai/gpt-4o 이 모델 말고 더 비싼 모델을 사용해도됨 

# 가드레일/필터링 (LLM모델이 생성되기 전 사용자의 입력에 대한 콜백)
def before_model_callback(
    callback_context : CallbackContext,
    llm_request :LlmRequest):
   
   history = llm_request.contents
   last_message = history[-1]
   if last_message.role == "user":
    text =  last_message.parts[0].text
    if "후무스" in text:  # 제외 텍스트 설정 
         #에러나 예외나 string을 반환하는게 아니라 공식문서에 보면 LLMresponse 타입을 리턴하라함 
         # 여기서 return하는건 모든지 llm이 보낸 메시지로 간주된다.
        return LlmResponse(
            content=types.Content( # llm이 보낸 응답보면 실제로 이런 구조임 (콘솔찍어서 보면나옴 or 위에 첫번째 예시 콘솔보면 ㅇㅇ)
                parts=[
                    types.Part(
                        text="죄송합니다. 그건 도와드릴 수 없습니다."
                    )
                ],
                role="model"
            )
        ) 
    return None

shorts_producer_agent = Agent(
    name = "ShortsProducerAgent",
    model = MODEL,
    description=SHORTS_PRODUCER_DESCRIPTION , 
    instruction=SHORTS_PRODUCER_PROMPT,
    tools=[
        AgentTool(agent=content_planner_agent),
        AgentTool(agent=asset_generator_agent),
        AgentTool(agent=video_assembler_agent),
    ],
    before_model_callback=before_model_callback # 미사용시 주석 후 사용 
)

root_agent = shorts_producer_agent