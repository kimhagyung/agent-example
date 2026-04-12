from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI 
from pydantic import BaseModel

from agents import Agent, Runner
agent = Agent(name="Assistant", instructions="You help users with their questions.")
 
# print(result.final_output)
 
app = FastAPI()

client = AsyncOpenAI()

class CreateConversationResponse(BaseModel):
    conversation_id : str

@app.post("/conversations")
async def create_conversation() -> CreateConversationResponse:
    conversation = await client.conversations.create()
    return {
        "conversation_id" : conversation.id,
    }

class CreateMessageInput(BaseModel):
    question: str

class CreateMessageOutput(BaseModel):
    answer : str 

@app.post("/conversations/{conversation_id}/message")
async def create_message(conversation_id : str, message_input : CreateMessageInput) -> CreateMessageOutput:
    answer = await Runner.run(
        starting_agent=agent, 
        input = message_input.question, 
        conversation_id=conversation_id,
    ) 
    return {
        'answer' : answer.final_output
    }

@app.post("/conversations/{conversation_id}/message-stream")
async def create_message(conversation_id : str, message_input : CreateMessageInput) -> CreateMessageOutput:
    async def event_generator(): 
        events =  Runner.run_streamed(
            starting_agent=agent, 
            input = message_input.question, 
            conversation_id=conversation_id,
        ) 
        async for event in events.stream_events():
            if event.type == "raw_response_event" and event.data.type == "response.output_text.delta":
                yield event.data.delta # yield를 쓰면 함수를 죽이지 않고 이 값을 함수 밖으로 뱉어낸다.(return을 쓰면 첫번째 함수에서 죽어버림)
                # 유저에게 보내고 싶은 이벤트를 yield로 보낸 

    return StreamingResponse(event_generator(), media_type="text/plain")
 
# 에이전트가 하는 모든것을 스트리밍 한다. 
@app.post("/conversations/{conversation_id}/message-stream-all")
async def create_message_all(conversation_id : str, message_input : CreateMessageInput) -> CreateMessageOutput:
    async def event_generator(): 
        events =  Runner.run_streamed(
            starting_agent=agent, 
            input = message_input.question, 
            conversation_id=conversation_id,
        ) 
        async for event in events.stream_events():
            if event.type == "raw_response_event":
                yield f"{event.data.to_json()}\n"

    return StreamingResponse(event_generator(), media_type="text/plain")
 