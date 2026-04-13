# AI Agents #21 Deploying Agents Final
## 1\. 프로젝트 목표

이 프로젝트는 OpenAI Agents SDK, LangGraph, 또는 Google SDK Agent를 배포하고 API를 통해 에이전트와 상호작용하는 방법을 다룬다.
FastAPI를 사용해 서버를 구축하며, Railway를 통해 최종 배포를 진행
  * 에이전트를 서버에 배포하는 프로세스를 이해
  * API를 통해 배포된 에이전트에 접근하고 실행하는 방법을 학습
  * FastAPI를 활용한 API 문서화 및 테스트 방법을 익힌다. 

-----

## 2\. 로컬 실행 및 설치

서버를 실행하고 로컬 환경에서 테스트하는 방법은 다음과 같다.

### **서버 실행**

```bash
uvicorn main:app --reload
```

  * 서버 실행 후 `http://127.0.0.1:8000/docs`에 접속하면 Swagger UI를 통해 API 명세를 확인가능 

### **API 테스트 도구**

  * **REST Client (VS Code Extension):** `.http` 파일을 작성하여 간편하게 요청을 보낼 수 있다. 설치 시 `Send Request` 버튼을 통해 즉시 테스트가 가능 
  * **StreamingResponse 테스트:** 스트리밍 응답의 경우 익스텐션에서 확인이 어려울 수 있으므로 터미널에서 `curl` 명령어를 직접 사용 
    ```bash
    curl -N -X POST http://127.0.0.1:8000/conversations/[CONVERSATION_ID]/message-stream \
         -H "Content-Type: application/json" \
         -d '{"question": "What is the size of the great wall of china?"}'
    ```

-----

## 3\. OpenAI Conversation API (메모리 관리)

기존에는 메시지 내역을 리스트(List) 형태의 변수에 담아 직접 관리했으나, 서버 배포 환경에서는 OpenAI의 **Conversation State** 기능을 활용 

  * **Conversation ID:** 대화를 생성하면 고유의 ID를 부여받는다.
  * **상태 관리:** 이후 요청 시 해당 ID를 함께 전달하면 OpenAI 서버에서 직접 대화 기록을 관리 
  * **장점:** 별도의 데이터베이스(DB) 구축이나 복잡한 메모리 관리 로직 없이도 대화 문맥을 유지 

-----

## 4\. Railway를 이용한 서버 배포

Railway는 서버 환경을 간편하게 배포할 수 있도록 도와주는 서비스이다. 다음 절차에 따라 배포를 진행한다.

### **Step 1: Railway CLI 설치 및 로그인**

터미널에서 Railway 사용을 위한 CLI를 설치하고 로그인한다.

```bash
npm i -g @railway/cli
railway login
```

### **Step 2: 프로젝트 설정 (`railway.json`)**

프로젝트 루트 디렉토리에 `railway.json` 파일을 생성하고 다음과 같이 설정한다. 이 설정은 Nixpacks를 빌더로 사용하며 서버 실행 명령어를 정의 

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT"
  }
}
```

### **Step 3: 프로젝트 초기화 및 배포**

명령어를 통해 Railway 프로젝트를 생성하고 코드를 업로드 

```bash
railway init
# Workspace 선택 및 프로젝트 이름(예: my-agent-deployment) 설정
railway up
```

### **Step 4: 도메인 설정 및 접속**

배포가 완료되면 [Railway Dashboard](https://www.google.com/search?q=https://railway.com/dashboard)에 접속하여 프로젝트를 선택 

1.  **Settings** 탭으로 이동 
2.  **Networking** 섹션에서 `Generate Domain` 버튼을 클릭 
3.  생성된 공용 URL을 복사하여 외부에서 API에 접근 

> **참고:** 현재 Railway 서비스는 유료 플랜으로 운영되므로 실제 테스트 시 과금 여부를 확인 
