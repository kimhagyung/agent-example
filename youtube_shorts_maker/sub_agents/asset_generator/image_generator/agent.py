from google.adk.agents import SequentialAgent
from .prompt_builder.agent import prompt_builder_agent
from .image_builder.agent import image_builder_agent 

image_generator_agent = SequentialAgent(   # 순차처리 
    name ="ImageGeneratorAgent",
    sub_agents=[
        # 프롬포트 작성 에이전트, 이미지 제작 에이전트 포함 (1. 대본작성 후 2. 이미지 생성)
        prompt_builder_agent,
        image_builder_agent
    ]
)
