from email import message
import dotenv
dotenv.load_dotenv()
from openai import OpenAI
import asyncio
import streamlit as st
from agents import  Runner, SQLiteSession, InputGuardrailTripwireTriggered
from models import UserAccountContext # 9.1에 추가  
from my_agents.triage_agent import triage_agent
 
client = OpenAI()

# 9.1에 추가 
user_account_ctx = UserAccountContext(
    customer_id=1,
    name="nico",
    tier="basic",
)


if "session" not in st.session_state:
    st.session_state["session"] = SQLiteSession(
        "chat-history",
        "customer-support-memory.db",
    )
session = st.session_state["session"] 

if "agent" not in st.session_state:
    st.session_state["agent"] = triage_agent

# 챗팅 UI에 대화 기록을 보여주는 함수 
async def paint_history():
    messages = await session.get_items()

    for message in messages:
        if "role" in message:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    content = message["content"]
                    if isinstance(content,str):                            
                        st.write(message["content"]) 
                else: # assistant 
                    if message["type"] == "message":
                        st.write(message["content"][0]["text"].replace("$", r"\$"))

asyncio.run(paint_history()) 


async def run_agent(audio_input):

    with st.chat_message("ai"): 
        text_placeholder = st.empty()
        response = ""

        st.session_state["text_placeholder"] = text_placeholder

        try:
            stream =  Runner.run_streamed(
                st.session_state["agent"], 
                message, 
                sesion= session,
                context = user_account_ctx 
                # runner에 context를 넣으니깐 이제 모든 function_tool들이 context를 받게 됨 (DI 의존성주입 같은거임 )
                # 위에다 넣으면 openai agents sdk가 모든 function_tool에 첫번쨰 argument로 넣어줄거임임(get_user_tier의 첫번쨰 ㅇㅇ)
            )

            async for event in stream.stream_events():
                    if event.type == "raw_response_event":  
                        if event.data.type == "response.output_text.delta":
                            response += event.data.delta
                            text_placeholder.write(response.replace("$", r"\$")) 
                    elif event.type == "agent_updated_stream_event":
                        if st.session_state["agent"].name != event.new_agent.name:
                            st.session_state["agent"] = event.new_agent  # 전환된 에이전트 업데이트 
                            st.write(f"Transfered from {st.session_state["agent"].name} to {event.new_agent.name}")
                            text_placeholder = st.empty() # 에이전트가 전환되면 전환된 에이전트에 맞는 입력창 생성 
                            response = ""
        except InputGuardrailTripwireTriggered:
            st.write("그건 도와줄 수없어")

  
message = st.chat_input(
    "Write a message for your assistant." 
)

if message:
    if "text_placeholder" in st.session_state:
        st.session_state["text_placeholder"].empty()

    if  message:
        pass
audio_input = st.audio_input(
    "Record your message",
)

if audio_input:

    with st.chat_message("human"):
        st.audio(audio_input)
    asyncio.run(run_agent(audio_input))


with st.sidebar:
    reset = st.button("Reset memory")
    if reset:
        asyncio.run(session.clear_session())
    st.write(asyncio.run(session.get_items()))