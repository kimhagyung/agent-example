 ## AI Agents #11 Google ADK Youtube Shorts Maker Agent

 ### **[.env 환경 파일 구성]**

이전과 동일


### **[목표]**

google adk의 Workflow Agents 를 사용하여 유튜브 쇼츠 메이커 에이전트 생성 

### **[Workflow Agents] 란? **
https://google.github.io/adk-docs/agents/workflow-agents/
sub-agents 의 실행 흐름을 제어하는 ​​특수 에이전트 
Workflow Agents는 ADK에서 sub-agents 의 실행 흐름을 조정하기 위해 특별히 설계된 구성 요소
주요 역할은 다른 에이전트가 실행되는 방법 과 시기 를 관리하고 프로세스의 제어 흐름을 정의하는 것이다. 
동적 추론 및 의사 결정을 위해 대규모 언어 모델(LLM)을 사용하는 LLM 에이전트 와 달리 , Workflow Agents는 미리 정의된 논리를 기반으로 작동
Workflow Agents는 오케스트레이션 자체를 위해 LLM을 참조하지 않고 유형(예: 순차, 병렬, 반복)에 따라 실행 순서를 결정한다. 결과적으로 실행 패턴은 결정론적이고 예측 가능

ADK는 각각 고유한 실행 패턴을 구현하는 세 가지 핵심 워크플로 에이전트 유형을 제공한다. 

1. sequential agent(https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/)
   -> sub agent들을 순차적으로 실행하게해주는 function
   -> sequential agent를 import하고 여러개의 sub agent를 넣으면 알아서 순차적으로 실행된다. 딱한번만 도는 loop임 
<img width="686" height="242" alt="image" src="https://github.com/user-attachments/assets/ec14f726-5278-494a-9e50-a24d95b8aa8d" />
2. Loop agents(https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/)
   -> sub-agent들을 반복해서 실행하는 agent이다. 
   -> 하나씩 차례로 실행하고 다시 반복함. autogen에서 썼던 round robin chat group이랑 거의 비슷함.
<img width="832" height="456" alt="image" src="https://github.com/user-attachments/assets/769c3149-68f2-4beb-9c9d-05c2fa12e2aa" />
3. Parallel agents(https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/)
   -> sub agent 리스트를 받아서 sub agent들을 병렬로 실행한다.
   <img width="538" height="256" alt="image" src="https://github.com/user-attachments/assets/59594007-d893-4d8c-8370-aeca4d4a0206" />


### **[실행방법]**
adk 설치 필요 
```bash 
   adk web
```

### **[사용 TOOL]**
tts로 사용 
https://platform.openai.com/docs/guides/text-to-speech
FFmpeg 사용 (생성된 이미지와 텍스트를 합쳐서 비디오로 만들어주는)
https://ffmpeg.org (설치필요)


