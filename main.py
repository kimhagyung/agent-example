import dotenv

dotenv.load_dotenv()
from openai import OpenAI
import asyncio
import streamlit as st
from agents import  Runner, SQLiteSession, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from models import UserAccountContext # 9.1에 추가  
from my_agents.triage_agent import triage_agent
from agents.voice import AudioInput, VoicePipeline
import numpy as np
import wave, io
from workflow  import CustomWorkflow
import sounddevice as sd # 이미 컴터에 깔려있음 

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
            audio = AudioInput(buffer=audio_array)
            # 2. custom workflow 생성 (stream을 실행할 떄 session이랑 context 그리고 session 에이전트랑 엮어서 돌리기 위해)
            workflow = CustomWorkflow(context=user_account_ctx)
            # 3. pipeline 생성  
            pipeline = VoicePipeline(workflow = workflow)

            status_container.update(label="Runner workflow", state="running")

            #pipeline 실행 
            result = await pipeline.run(audio)

            player = sd.OutputStream(
                samplerate=24000,
                channels = 1, 
                dtype = np.int16
            )
            player.start()

            status_container.update(state="complete")

            # 스트리밍 방식으로 실시간 번역 함 
            async for event in result.stream():
                if event.type == 'voice_stream_event_audio': # 새로운 오디오 조각 왔다는 뜻 
                    player.write(event.data)


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
    asyncio.run(run_agent(audio_input))

with st.sidebar:
    reset = st.button("Reset memory")
    if reset:
        asyncio.run(session.clear_session())
    st.write(asyncio.run(session.get_items()))