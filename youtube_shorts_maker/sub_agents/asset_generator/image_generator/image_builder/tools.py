from google.adk.tools.tool_context import ToolContext


def generate_images(tool_context:ToolContext): # tool_context 는 결과값에서 state > prompt_builder_output 부분의 값이다. 
     
    # 1. prompt_builder_output 가져오기 
    prompt_builder_agent = tool_context.state.get("prompt_builder_output")
    # 2. prompt_builder_output>  optimized_prompts 가져오기 
    optimized_prompts = tool_context.state.get("optimized_prompts")
