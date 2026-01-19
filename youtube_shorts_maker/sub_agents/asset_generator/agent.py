from google.adk.agents import ParallelAgent  # 병렬처리 
from .prompt import ASSET_GENERATOR_DESCRIPTION
from .image_generator.agent import image_generator_agent
from .voice_generator.agent import voice_generator_agent

asset_generator_agent = ParallelAgent(
    name = "AssetGeneratorAgent",
    description= ASSET_GENERATOR_DESCRIPTION ,
    sub_agents = [ # 동시에 실행 
        image_generator_agent,
        voice_generator_agent,
    ]

)
