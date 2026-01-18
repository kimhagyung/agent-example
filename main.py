from email import message
import dotenv

dotenv.load_dotenv()
from openai import OpenAI
import asyncio
import streamlit as st
from agents import (
    Runner,
    SQLiteSession,
    function_tool, 
    RunContextWrapper 
)
from agents.voice import AudioInput, VoicePipeline
from models import UserAccountContext # 9.1에 추가  

# 해당 tool을 모든 에이전트들에게 줄 수 있음 . 모든 에이전트들에게 줄 수없으니 올바른 context에 접근할 수 있는 tool을 주고싶
# 예를들어 환불 에이전트면 tool을 만들어서 에이전트가 오직 재무 거래만 가져올 수 있도록 
# 구매 정보 에이전트면 구매관련 정보만 가져오는 tool을 만들거나 ㅇㅇ 
@function_tool
def get_user_tied(wrapper : RunContextWrapper[UserAccountContext]):  # wrapper로 넣는 이유는 
    # 아래 context = user_account_ctx  을 해줬기에 해당 get_user_tied tools로 context를 가져올 수 있음 
    return  f"The user {wrapper.context.customer_id} has a {wrapper.context.tier} account" # 이 고객 아이디는 이 등급의 계정을 가지고 있습니다. 
 
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

        stream =  Runner.run_streamed(
            agent, 
            message, 
            sesion= session
            context = user_account_ctx 
             # runner에 context를 넣으니깐 이제 모든 function_tool들이 context를 받게 됨 (DI 의존성주입 같은거임 )
             # 위에다 넣으면 openai agents sdk가 모든 function_tool에 첫번쨰 argument로 넣어줄거임임(get_user_tier의 첫번쨰 ㅇㅇ)
        )

        async for event in stream.stream_events():
                if event.type == "raw_response_event": 
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