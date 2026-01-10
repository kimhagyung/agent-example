import base64
from google.genai import types
from openai import OpenAI
from google.adk.tools.tool_context import ToolContext

client = OpenAI()


async def generate_images(tool_context: ToolContext): # tool_context 는 결과값에서 state > prompt_builder_output 부분의 값이다. 

    # 1. status 값 추출
    # 1. prompt_builder_output 가져오기
    prompt_builder_output = tool_context.state.get("prompt_builder_output")
    # 2. prompt_builder_output>  optimized_prompts 가져오기 
    optimized_prompts = prompt_builder_output.get("optimized_prompts")

    # 2. 기존 artifacts를 리스트업 (생성된 이미지를 재생성하지 않기 위해)
    existing_artifacts = await tool_context.list_artifacts()

    generated_images = [] # 생성된 이미지 정보 넣을 리스트 

    # 3. artifacts bucket 에 어떤 images 가 이미 있는지 확인  
    for prompt in optimized_prompts:
        scene_id = prompt.get("scene_id")
        enhanced_prompt = prompt.get("enhanced_prompt")
        filename = f"scene_{scene_id}_image.jpeg" # 파일이 이미 존재하는ㄴ지 확인 할 때 사용하는 파일명 생성 


        if filename in existing_artifacts: # 존재확인 

            generated_images.append(
                {
                    "scene_id": scene_id,
                    "prompt": enhanced_prompt[:100],
                    "filename": filename,
                }
            )
            continue

        # 생성되지 않았다면 이미지 생성 
        image = client.images.generate(
            model="gpt-image-1", # 이미지 안에 글씨 적ㅇ기좋음 
            prompt=enhanced_prompt,
            n=1,
            quality="low",   # 돈 덜쓰고 빨리됨 
            moderation="low",
            output_format="jpeg",
            background="opaque",
            size="1024x1536",
        ) # 이미지 생성 끝 


        image_bytes = base64.b64decode(image.data[0].b64_json) # 응답 이미지 디코드 

        artifact = types.Part(
            inline_data=types.Blob(
                mime_type="image/jpeg",
                data=image_bytes,
            )
        )

        # 파일 저장
        await tool_context.save_artifact(
            filename=filename,
            artifact=artifact,
        )

        # 생성된 이미지에 대한 정보를 리스트에 추가 
        generated_images.append(
            {
                "scene_id": scene_id,
                "prompt": enhanced_prompt[:100],
                "filename": filename,
            }
        )

    return {
        "total_images": len(generated_images),
        "generated_images": generated_images,
        "status": "complete",
    }