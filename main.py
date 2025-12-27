import dotenv 
dotenv.load_dotenv()
import time 
import asyncio # await과 같은 의미 
import streamlit as st 
from agents import Agent, Runner, SQLiteSession, WebSearchTool

if "agent" not in st.session_state: # agent 재생성 방지
    st.session_state["agent"] = Agent(
        name = "ChatGPT Clone",
        instructions="""
            You are a helpful assistant.

            You have access to the following tools:
                - Web Search Tool: Use this when the user asks a questions that isn't in your training data. 
                Use this to learn about current events.
        """, 
        tools =[WebSearchTool()],
        
    )
agent = st.session_state["agent"]

#세션 반복 생성 방지를 위해 "session_state" 가 없으면 세션 초기화  (처음 한번 생성)
if "session" not in st.session_state:
    st.session_state["session"] = SQLiteSession("chat-history", "chat-gpt-clone-memory.db")
session = st.session_state["session"]

# 챗팅 UI에 대화 기록을 보여주는 함수 
async def paint_history():
    messages = await session.get_items()

    for message in messages:
        if "role" in message:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.write(message["content"])
                else: # assistant 
                    if message["type"] == "message":
                        st.write(message["content"][0]["text"])
        if "type" in message and message["type"] == "web_search_call":
            with st.chat_message("ai"):
                st.write("🔎Searched the Web...") 

# 상태 업데이트 
def update_status(status_container, event):
    
    status_messages = {
         "response.web_search_call.completed" :("✅ Web search completed.","complete"),
          "response.web_search_call.in_progres" : ("🔎 Starting web search...","running"),
          "response.web_search_call.searching" : ("🔎 Web search in progress...","running"),
          "response.completed" : (" ","complete")
    }

    if event in status_messages:
        label, state = status_messages[event]
        status_container.update(label=label, state=state)
  
asyncio.run(paint_history())  # 이 함수로 인해 대화ui가 계속 이어짐. 없으면 기존 대화가 덮힘 (뭔말인지 모르겠으면 없애봐도됨)

async def run_agent(message):
    with st.chat_message("ai"):
        text_placeholder = st.empty() #비어있는 컨테이너 만들기 
        response = "" 

        status_container  = st.status("⌛", expanded=False) 
        stream = Runner.run_streamed(agent, message,session = session)

        async for event in stream.stream_events():
            if event.type == "raw_response_event":

                update_status(status_container, event.data.type)

                if event.data.type == "response.output_text.delta":
                    response += event.data.delta
                    text_placeholder.write(response)

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