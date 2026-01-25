from email import message
import dotenv
dotenv.load_dotenv()
from openai import OpenAI
import asyncio
import streamlit as st
from agents import  Runner, SQLiteSession, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from models import UserAccountContext # 9.1에 추가  
from my_agents.triage_agent import triage_agent
from agents.voice import AudioInputs
import numpy as np
import wave, io
 
client = OpenAI()

# 9.1에 추가 
user_account_ctx = UserAccountContext(
    customer_id=1,
    name="nico",
    tier="basic",
    email="nico@las.com" 
)


if "session" not in st.session_state:
    st.session_state["session"] = SQLiteSession(
        "chat-history",
        "customer-support-memory.db",
    )
session = st.session_state["session"] 

if "agent" not in st.session_state:
    st.session_state["agent"] = triage_agent

def convert_audio(audio_input):
    audio_data = audio_input.getvalue()
    
    with wave.open(io.BytesIO(audio_data), "rb") as wav_file:
        audio_frames = wav_file.readframes(-1)

    return np.frombuffer(
        audio_frames,
        dtype = np.int16
    )

async def run_agent(audio_input):

    with st.chat_message("ai"): 
         
        status_container = st.status("⌛ Processing voice message...") 
        try:

            # 1. audio -> numpy 배열로 변환 
            audio_array = convert_audio(audio_input)
            # audio 파일 객체 생성 
            audio = AudioInputs(buffer=audio_array)
            # 2. custom workflow 생성 (stream을 실행할 떄 session이랑 context 그리고 session 에이전트랑 엮어서 돌리기 위해)
            
            # 3. pipeline 생성 

            stream =  Runner.run_streamed(
                st.session_state["agent"], 
                message, 
                session= session,
                context = user_account_ctx 
                # runner에 context를 넣으니깐 이제 모든 function_tool들이 context를 받게 됨 (DI 의존성주입 같은거임 )
                # 위에다 넣으면 openai agents sdk가 모든 function_tool에 첫번쨰 argument로 넣어줄거임임(get_user_tier의 첫번쨰 ㅇㅇ)
            ) 
                  
        except InputGuardrailTripwireTriggered:  
            st.write("사용자의 요청에서 부적절한 내용이 감지되어 중단되었습니다.")
        except OutputGuardrailTripwireTriggered:  
            st.write("보안 정책상 부적절한 답변이 감지되어 내용을 표시할 수 없습니다.")
        
  
audio_input = st.audio_input(
    "Record your message" 
)

if audio_input: 
    with st.chat_message("human"):
        st.audio(audio_input)
    asyncio.run(run_agent(message))

with st.sidebar:
    reset = st.button("Reset memory")
    if reset:
        asyncio.run(session.clear_session())
    st.write(asyncio.run(session.get_items()))