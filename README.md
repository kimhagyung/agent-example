## AI Agents #11 Google ADK Youtube Shorts Maker Agent

### **[.env 환경 파일 구성]**

* 이전 프로젝트와 동일

---

### **[목표]**

* Google ADK의 **Workflow Agents**를 사용하여 유튜브 쇼츠 제작 에이전트 생성

---

### **[Workflow Agents] 란?**

[공식 문서](https://google.github.io/adk-docs/agents/workflow-agents/)

* Sub-agents의 실행 흐름을 제어하는 특수 에이전트
* ADK에서 서브 에이전트들의 실행 흐름을 조정하기 위해 설계된 구성 요소임
* **주요 역할:** 다른 에이전트가 실행되는 **방법**과 **시기**를 관리하고 프로세스의 제어 흐름(Control Flow)을 정의함
* **특징:** 동적 추론을 위해 LLM을 사용하는 일반 에이전트와 달리, Workflow Agents는 **미리 정의된 논리(Logic)**를 기반으로 작동함
* 오케스트레이션 자체를 위해 LLM을 호출하지 않고 유형(순차, 병렬, 반복)에 따라 실행 순서를 결정하기 때문에, 실행 패턴이 **결정론적(Deterministic)이고 예측 가능**함

#### **핵심 워크플로 에이전트 3가지 유형**

**1. Sequential Agent**
[문서 링크](https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/)

* Sub-agents를 순차적으로 실행하게 해주는 기능
* Sequential Agent를 import하고 여러 개의 Sub-agent를 리스트로 넣으면 알아서 순차적으로 실행됨 (정해진 순서대로 딱 한 번 실행되는 구조)

<img width="686" alt="image" src="https://github.com/user-attachments/assets/ec14f726-5278-494a-9e50-a24d95b8aa8d" />

**2. Loop Agents**
[문서 링크](https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/)

* Sub-agents를 반복해서 실행하는 에이전트
* 에이전트들을 하나씩 차례로 실행하고 다시 처음으로 돌아가 반복함. Autogen에서 썼던 **Round Robin Chat Group**이랑 거의 비슷하다고 보면 됨

<img width="832" alt="image" src="https://github.com/user-attachments/assets/769c3149-68f2-4beb-9c9d-05c2fa12e2aa" />

**3. Parallel Agents**
[문서 링크](https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/)

* Sub-agent 리스트를 받아서 여러 에이전트를 동시에(병렬로) 실행함

<img width="593" height="290" alt="image" src="https://github.com/user-attachments/assets/6909c57a-4d75-4753-ae52-39ef258c6264" />


---

### **[실행 방법]**

* ADK 설치 후 아래 명령어 실행

```bash
adk web

```

---

### **[사용 TOOL]**

* **OpenAI TTS:** 텍스트를 음성으로 변환할 때 사용 ([문서](https://platform.openai.com/docs/guides/text-to-speech))
* **FFmpeg:** 생성된 이미지와 오디오를 합쳐서 최종 쇼츠 비디오로 렌더링 ([공식 사이트](https://ffmpeg.org))
* *참고: 로컬 시스템에 FFmpeg 설치가 반드시 되어 있어야 함*

