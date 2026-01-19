from pydantic import BaseModel, ConfigDict, Field # 필드드에 대한 설명 
from typing import List

# prompt.py에 기입한 우리 원하는 모양(JSON)과 딱 맞는지 
class SceneOutput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: int = Field(description="Scene ID number")
    narration: str = Field(description="Narration text for the scene")
    visual_description: str = Field(
        description="Detailed description for image generation"
    )
    embedded_text: str = Field(
        description="Text overlay for the image (can be any case/style)"
    )
    embedded_text_location: str = Field(
        description="Where to position the text on the image (e.g., 'top center', 'bottom left', 'middle right', 'center')"
    )
    duration: int = Field(description="Duration in seconds for this scene")

# 프롬포트에 있는 json형식의 반환값에 대한 형식 지정 
class ContentPlanOutput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    topic: str
    total_duration: int
    scenes: List[SceneOutput]