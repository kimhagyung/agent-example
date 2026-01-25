from agents.voice import VoiceWorkflowBase, VoiceWorkflowHelper
from agents import Runner 
import streamlit as st 

class CustomWorkflow(VoiceWorkflowBase):
    def __init__(self, context):
        self.context = context 

    async def run(self, transcription): # 여기서 텍스트를 받는다.
        result = Runner.run_streamed(
            st.session_state["agent"], 
            transcription,   # voice pipeline이 준 유저 음성의 transcription으로 처리함 
            session= st.session_state["session"],
            context = self.context
        ) 
        # 1. transcription을 받는다. 
        # 2. 마치 유저가 키보드에서 입력한 것처럼 runner을 돌린다. 

        # 에이전트의 응답을 pipeilne에 넘겨준다 , SingleAgentVoiceWorkflow문서에 있음 
        async for chunk in VoiceWorkflowHelper.stream_text_from(result):
            yield chunk # 텍스트를 pipeline에 스트리밍으로 돌려주는 방식임 

        st.session_state["agent"]  = result.last_agent # 이거 전에 다른 에이전트로 handoff 되고 다음 대화부터 다시 메인 에이전트로 돌아오지 않도록 하기위해