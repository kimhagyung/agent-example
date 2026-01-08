from google.adk.agents import Agent 
from google.adk.models.lite_llm import LiteLlm
from .prompt import IMAGE_BUILDER_DESCRIPTION, IMAGE_BUILDER_PROMPT
from .tools import generate_images

MODEL = LiteLlm(model="openai/gpt-4o")

image_builder_agent = Agent( # 출력 자체는 그냥 메시지 일것임 
    name ="ImageBuilder",
    description=IMAGE_BUILDER_DESCRIPTION,
    instruction=IMAGE_BUILDER_PROMPT,
    model = MODEL ,
    output_key = "image_builder_output", # 출력자체는 그냥 메시지인데 그냥 이미지 완성되었다는 메시지로 ㅇㅇ 
    tools=[  
        generate_images
    ] # tool 이름은 prompt에 있는 tool의 이름과 같아야함. 
)