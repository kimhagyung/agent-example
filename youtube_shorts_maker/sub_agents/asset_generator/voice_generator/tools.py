from google.genai import types
from openai import OpenAI
from google.adk.tools.tool_context import ToolContext
from typing import List, Dict, Any 

client = OpenAI()

# 1. 모델이 state에 있는 값을 가져온다. ({content_planner_output} 을 보고 )
async def generate_narrations(
    tool_context : ToolContext ,  voice : str, 
    voice_instructions : List[Dict[str, Any]]
):

 # prompt.py 에도 설명이 되어있긴 하지만 아래 doc string 위에 변수가 뭘 해야되는건지 한번더 써주겟삼
  """
    Generate narration audio for each scene using OpenAI TTS API

    Args:
        tool_context: Tool context to access artifacts and save files
        voice: Selected voice for TTS (alloy, echo, fable, onyx, nova, shimmer)
        voice_instructions: List of dictionaries containing narration instructions for each scene

    Returns:
        Information about all generated audio files
  """

  # 기존 artifact 를 조회
  existing_artifacts = await tool_context.list_artifacts()
  # existing_artifacts가 객체 리스트일 경우 파일명 추출 (필요 시 수정)
  existing_filenames = [a.filename for a in existing_artifacts] if existing_artifacts else []

  generated_narrations = []

  for instruction in voice_instructions:
        text_input = instruction.get("input")
        instructions = instruction.get("instructions")
        scene_id = instruction.get("scene_id")
        filename = f"scene_{scene_id}_narration.mp3"

        if filename in existing_filenames:
          generated_narrations.append( # 존재한다면 정보 리스트에 ㅈ추가 
                  {
                      "scene_id": scene_id,
                      "filename": filename,
                      "input": text_input,
                      "instructions": instructions[:50] if instructions else "",
                  }
              )
          continue

        with client.audio.speech.with_streaming_response.create(
          model="gpt-4o-mini-tts",  
          voice=voice, # 목소리 
          input=text_input, # 읽을 문장 
          # OpenAI 공식 TTS API는 현재 별도의 instructions 파라미터를 지원하지 않으므로 주의가 필요합니다.
        )as response:
          audio_data = response.read()

        artifact = types.Part(
            inline_data=types.Blob(mime_type="audio/mpeg", data=audio_data)
        )

        await tool_context.save_artifact( filename=filename,artifact=artifact)

        generated_narrations.append( # 존재한다면 정보 리스트에 ㅈ추가 
            {
                "scene_id": scene_id,
                "filename": filename,
                "input": text_input,
                "instructions": instructions[:50] if instructions else "",
            }
        )

  # (모든 장면 생성을 완료한 뒤 반환)
  return {
      "success": True,
      "narrations": generated_narrations,
      "total_narrations": len(generated_narrations),
  }