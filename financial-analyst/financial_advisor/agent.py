from google.adk.agents import Agent 
from google.adk.models.lite_llm import LiteLlm

MODEL = LiteLlm("openai/gpt-4o")

weather_agent = Agent(
    name ="WeatherAgent",
    instruction="You help the user with weather related questions",  # 너는 날씨 관련 질문을 받아서 사용자를 도와줄거야 
    model = MODEL
)

# 반드시 있어야 하는 변수임 
root_agent = weather_agent