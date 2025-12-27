import dotenv 
dotenv.load_dotenv()
import asyncio # await과 같은 의미 
import streamlit as st 
from agents import Agent, Runner, SQLiteSession

if "agent" not in st.session_state: # agent 재생성 방지
    st.session_state["agent"] = Agent(
        name = "ChatGPT Clone",
        instructions="""
            You are a helpful assistant.
        """
    )
agent = st.session_state["agent"]

#세션 반복 생성 방지를 위해 "session_state" 가 없으면 세션 초기화  (처음 한번 생성)
if "session" not in st.session_state:
    st.session_state["session"] = SQLiteSession("chat-history", "chat-gpt-clone-memory.db")
session = st.session_state["session"]

async def run_agent(message):
    stream = Runner.run_streamed(agent, message,session = session)

    async for event in stream.stream_events():
        if event.type == "raw_response_event":
            if event.data.type == "response.output_text.delta":
                with st.chat_message("ai"):
                    st.write(event.data.delta)



prompt = st.chat_input("Write a message for your assistant")

if prompt: 
    with st.chat_message("user"):
        st.write(prompt) #메시지를 치면 user아이콘으로 화면에 보이게 함 
    asyncio.run(run_agent(prompt))
    
# 내 챗봇의 메모리를 볼 수 있는 디버깅 사이드바 만들기 , 또한 대화를 다시 시작하고 싶을 때를 위해 session을 지우는 버튼도 만든다. \
with st.sidebar:
    reset = st.button("Reset memory")
    if reset: # 버튼이 클릭됐을 때(True)
        asyncio.run(session.clear_session())  #session 지워짐 
    st.write(asyncio.run(session.get_items())) 