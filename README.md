## AI Agents #12 Google ADK Deep Dive

### **[.env 환경 파일 구성]**

* 이전과 동일

### **[목표]**

* **프로덕션용 Agent 구축:** 개발용 Web UI를 벗어나 실제 서비스 환경에서 실행되는 Agent 개발.
* **성능 평가:** ADK 내장 기능을 활용한 에이전트 성능 검증 방법 습득.
* **API 연동:** 자동 생성된 API 서버를 활용하여 커스텀 프론트엔드와 에이전트 연결.

### **[Agent 평가 방법]**

* LLM 특성상 입력 대비 출력이 유동적이므로, 기존 소프트웨어 테스트와는 다른 방식이 필요함.

1. **Tool Trajectory (도구 실행 경로) 테스트**
* **핵심:** 에이전트가 도구를 호출하는 '순서'와 '과정'을 검증.
* **용도:** 특정 지침(Instruction)에 따라 도구 A 다음 도구 B를 반드시 호출해야 하는 시나리오에서 유용함.


2. **최종 응답 (Final Response) 테스트**
* **핵심:** 중간 과정보다는 사용자에게 전달되는 '결과값'의 정확도를 검증.
* **용도:** 도구 사용 순서와 상관없이 최종 답변의 품질이 중요할 때 사용.



### **[API 실행 방법]**

1. **라이브러리 설치:** `uv add requests`
2. **서버 실행:** `adk api_server`
3. **Swagger UI 확인:** `http://127.0.0.1:8000/docs`
* **주의:** 접속 오류 발생 시 Python 버전을 **3.13 미만**으로 낮추는 것을 권장.



### **[Invocation Flow]**

> [ADK Invocation Flow Diagram](https://google.github.io/adk-docs/assets/invocation-flow.png)

### **[Vertex AI Agent Engine 배포]**

> [Deployment Guide](https://google.github.io/adk-docs/deploy/agent-engine/)

* **개념:** Google Cloud에서 제공하는 AI Agent 전용 완전 관리형 배포 서비스.
* **특징:** 프로덕션 환경에서 에이전트 관리 및 확장성 확보 가능.

**[사전 준비]**

1. [Google Cloud CLI](https://docs.cloud.google.com/sdk/docs/install-sdk#windows) 설치 및 인증.
2. [GCS 버킷 생성](https://console.cloud.google.com/storage/browser).
3. 가상환경 라이브러리 추가: `uv add "google-cloud-aiplatform[adk,agent_engines]" cloudpickle`
4. [AI Platform API](https://console.cloud.google.com/flows/enableapi?apiid=aiplatform.googleapis.com) 활성화.

**[배포 실행]**

```bash
# 구글 권한 인증 및 프로젝트 설정
gcloud auth application-default login --project [project-id]
gcloud config set project [project-id]

# 배포 스크립트 실행
uv run deploy.py

```

### **[설치 리스트]**

* `uv add requests`
* `pip install aiosqlite`
* `uv add "google-cloud-aiplatform[adk,agent_engines]"`
* `uv add cloudpickle`
