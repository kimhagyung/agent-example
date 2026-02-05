## AI Agents #12 Google ADK Deep Dive

### **[.env 환경 파일 구성]**

* 이전과 동일

### **[목표]**

* **프로덕션용 Agent 구축:** 개발 전용 UI가 아닌 실제 서비스 환경에서 동작하는 Agent 개발.
* **성능 평가:** ADK 내장 기능을 사용해 에이전트의 답변 품질과 도구 사용 순서 검증.
* **API 연동:** 직접 만든 프론트엔드에서 API를 통해 에이전트를 실행하고 스트리밍 업데이트 확인.

### **[Agent 평가 방법]**

* **Tool Trajectory (도구 실행 경로) 테스트**
* **핵심:** 에이전트가 도구를 호출하는 '순서'와 '과정'을 검증.
* **용도:** "A 도구 실행 후 반드시 B 도구를 호출해야 한다"는 로직이 있을 때 유용.


* **최종 응답 (Final Response) 테스트**
* **핵심:** 도구 사용 과정과 관계없이 사용자에게 전달되는 '최종 결과'의 정확도만 확인.



### **[API 실행 방법]**

1. **라이브러리 설치:** `uv add requests`
2. **서버 실행:** `adk api_server`
3. **Swagger UI 확인:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **참고:** 접속 오류 시 Python 버전을 3.13 미만으로 낮추는 것을 추천함. (이슈 관련 링크: [https://github.com/google/adk-python/issues/3173](https://github.com/google/adk-python/issues/3173))



### **[Invocation Flow]**

* **다이어그램 링크:** [https://google.github.io/adk-docs/assets/invocation-flow.png](https://google.github.io/adk-docs/assets/invocation-flow.png)

### **[Vertex AI Agent Engine 배포]**

* **가이드 링크:** [https://google.github.io/adk-docs/deploy/agent-engine/](https://google.github.io/adk-docs/deploy/agent-engine/)
* **개념:** Google Cloud의 완전 관리형 서비스를 활용해 프로덕션급 에이전트를 배포 및 확장.

**[사전 준비 단계]**

1. **Google Cloud CLI 설치:** [https://docs.cloud.google.com/sdk/docs/install-sdk#windows](https://docs.cloud.google.com/sdk/docs/install-sdk#windows)
2. **인증:** 설치 후 콘솔 창에서 구글 계정 인증 진행.
3. **버킷 생성:** [https://console.cloud.google.com/storage/browser](https://console.cloud.google.com/storage/browser) (결과물 저장용)
4. **API 활성화:** [https://console.cloud.google.com/flows/enableapi?apiid=aiplatform.googleapis.com](https://console.cloud.google.com/flows/enableapi?apiid=aiplatform.googleapis.com)

**[배포 실행 명령]**

```bash
# 프로젝트 권한 설정 및 로그인
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
 
