## AI Agents #9 OpenAI Agents SDK Customer Support Agent

### **[.env 환경 파일 구성]**

* 이전과 동일

### **[목표]**

* 고객지원(Customer Support) 에이전트 구축

### **[목적]**

* **서비스 필수 요소:** 고객 대상 서비스를 계획한다면 반드시 필요함.
* **대화 검열:** 유저들이 LLM을 단순히 개인적인 ChatGPT처럼 사용하지 못하도록 주제를 제한해야 함.
* **데이터 연동:** 대화 시작 전 고객 기본 정보, 구매 이력 등 서비스 운영에 필요한 데이터를 사전에 확보하고 있어야 함.

### **[Context]**

> [OpenAI Agents SDK - Context](https://openai.github.io/openai-agents-python/context/)

* **데이터 전달:** 유저 계정 정보 등은 내부적으로 모든 '보조 에이전트'에 전달됨. 이것이 Context의 역할.
* **Tool과의 관계:** Context 데이터를 에이전트에게 직접 넘기는 것이 아니라, **Tools에게 전달**함.
* 즉, Tool을 만들어서 Context 내의 특정 데이터를 꺼내 쓰는 방식.


* **범위:** Context가 볼 수 있는 데이터는 기본적으로 '대화 기록'임. (단순히 AI에게 모든 걸 한 번에 넘기는 구조가 아님)

<img width="545" height="308" alt="image" src="[https://github.com/user-attachments/assets/09513eef-4ab9-48c0-b320-d5b6b88dc6e2](https://github.com/user-attachments/assets/09513eef-4ab9-48c0-b320-d5b6b88dc6e2)" />

### **[Guardrails]**

> [Guardrails Example Code](https://github.com/kimhagyung/agent-example/commit/227029483121e0638c66d34fa2151826c135e6b2)

* **주제 이탈 방지:** 자사 서비스와 관련 없는 대화로 인한 어마어마한 토큰 비용 낭비를 막음.
* **Guardrails 종류:**
1. **입력(Input) Guardrails:** 유저의 질문이 적절한지 검사.
2. **출력(Output) Guardrails:** 에이전트의 답변을 별도의 에이전트가 규칙에 따라 검토.


* **Tripwire (경보 장치):**
* 에이전트가 정해진 규칙을 어기면 작동함.
* Tripwire가 작동한다는 것은 더 이상 대화를 진행하면 안 된다는 신호임.
* 답변이 부적절할 경우 출력을 차단하고 대화를 중단시킴. 
