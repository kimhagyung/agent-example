from google.adk.agents import Agent 
from google.adk.models.lite_llm import LiteLlm
from pydantic import ConfigDict
# 모든 모델에 대해 임의 타입 허용 설정 (필요 시)
ConfigDict(arbitrary_types_allowed=True)
MODEL = LiteLlm("openai/gpt-4o")

def get_weather(city: str) -> str:
    return f"The weather in {city} is 30 degrees"

def convert_units(degrees: int) -> str:
    return f"That is 40 farenheit"

geo_agent = Agent(
    name = "GeoAgent",
    instruction= "You help with geo questions",
    description= "Transfer to this agent when you have a geo related question"
    # root agent(weather_agent)가 해당 agent의 설명을 읽어야 해서 ! root agent를 위한 설명임 
    # 그래야 언제 transfer해야 하는지 알게 됨 
)

weather_agent = Agent(
    name ="WeatherAgent",
    instruction="You help the user with weather related questions",  # 너는 날씨 관련 질문을 받아서 사용자를 도와줄거야 
    model = MODEL,
    tools=[get_weather,convert_units],
    sub_agents=[ # openai sdk 에서 handoff랑 같음 
        geo_agent
    ]
)

# 반드시 있어야 하는 변수임 
root_agent = weather_agent