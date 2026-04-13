# AI Agents #20: A2A (Agent-to-Agent) Study

## 1. 환경 설정 (.env)
* **OPENAI_API_KEY** 설정

---

## 실행 방법 (How to Run)
원활한 테스트를 위해 콘솔 창 2개

1.  **Client Agent 실행**
    ```bash
    cd user-facing-agent
    adk web
    ```
2.  **Remote Agent 실행**
    ```bash
    cd remote_adk_agent
    uvicorn agent:app --port 8001
    ```
3.  **접속 확인**
    * [http://127.0.0.1:8001/.well-known/agent-card.json](http://127.0.0.1:8001/.well-known/agent-card.json) 접속해서 JSON 나오는지 체크!

---

## A2A 란?
> 참고: [a2a-protocol.org](https://a2a-protocol.org/latest/topics/what-is-a2a/#a2a-and-adk)

**A2A (Agent to Agent Communication Protocol)** 는 이름 그대로 에이전트끼리 서로 소통하게 해주는 프로토콜

* **Main Agent:** 사용자와 직접 대화하는 에이전트.
* **Sub Agent:** 다른 서버에 호스팅 되어 있는 에이전트들.
    * Google ADK로 만든 Agent (2개) + LangGraph로 만든 Agent (1개) 구성
* **특이사항:** 현재 A2A 구현에 가장 최적화된 프레임워크는 **Google ADK**이다.
    * 나의 Agent를 A2A 서버로 변환하거나, Main Agent를 원격 에이전트에 연결하는 함수/클래스가 잘 되어 있다.

---

## A2A For Dummies (동작 원리)

### **1단계: Agent Discovery (에이전트 찾기)**
* Client Agent가 Remote Agent Server의 `/.well-known/agent-card.json` URL로 GET 요청을 보낸다
* 서버는 해당 에이전트의 **동작 방식, 보유 스킬** 등이 담긴 JSON 결과를 반환함. (필요 시 인증 진행)

### **2단계: sendMessage API (메시지 전송)**
* Client Agent가 확인된 URL(예: `http://localhost:8001`)로 메시지를 보낸다
* Remote Agent Server는 즉시 **Task Response**를 반환.
    * 여기에는 Task의 **ID**와 현재 **Status**가 포함.

### **3단계: sendMessageStream API (상태 업데이트)**
* Client Agent가 서버에 업데이트를 계속 요청하거나, Remote Agent Server가 스트리밍 방식으로 데이터를 쏴준다.
* 이 모든 과정은 `to_a2a` 함수 하나로 간편하게 처리된다.
    * `app = to_a2a(agent, port=8001)`
    * 이 서버가 Task로 응답하고, 완료되거나 업데이트가 있을 때마다 Client(`user_facing_agent`)로 스트림을 보내주는 구조

---

## API 상세 (FastAPI Server)

### **SendMessagesResponse**
반환 타입은 크게 **Task** 또는 **Message**로 나뉜다.

| 타입 | 설명 |
| :--- | :--- |
| **Task** | 비동기 작업의 ID와 진행 상태를 포함 |
| **Message** | 에이전트가 생성한 실제 텍스트나 데이터 결과값 |

> 자세한 타입 명세는 [A2A 공식 문서](https://a2a-protocol.org/latest/sdk/python/api/a2a.types.html#a2a.types.SendMessageSuccessResponse)를 참고.
