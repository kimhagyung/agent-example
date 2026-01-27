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

<img width="545" height="308" alt="image" src="https://github.com/user-attachments/assets/e2a7190e-6eac-4a59-b116-35a844f0e8c1" />

### **[Guardrails]**

> [Guardrails Example Code](https://github.com/kimhagyung/agent-example/commit/227029483121e0638c66d34fa2151826c135e6b2)

* **주제 이탈 방지:** 자사 서비스와 관련 없는 대화로 인한 불필요한 토큰 비용 낭비를 방지함.
* **Guardrails 종류:**
1. **입력(Input) Guardrails:** 유저의 질문이 서비스 목적에 적절한지 사전에 검사.
2. **출력(Output) Guardrails:** 에이전트의 답변을 별도의 에이전트가 규칙에 따라 최종 검토.


* **참고:** Input과 Output Guardrails는 적용 시점만 다를 뿐, 검증 로직 자체는 유사한 개념임.


### **[Tripwire (경보 장치)]**
* 에이전트가 정해진 규칙(보안, 정책 등)을 어기려고 할 때 즉각 작동하는 안전장치.
* Tripwire가 작동했다는 것은 시스템이 위험을 감지하여 더 이상 대화를 진행하면 안 된다는 신호임.
* 부적절한 답변이 생성될 경우 출력을 즉시 차단하고 대화를 중단시킴.


### **[Handoffs]**
* 대화의 제어권 자체를 다른 전문 에이전트에게 완전히 넘기는 방식.
* **비유:** 콜센터에서 담당 부서가 아닐 경우 다른 부서로 전화를 연결해 주는 것과 같음.
* **차이점:** 만약 Handoff가 아닌 'Tool'로서 에이전트를 호출했다면, 상담원이 전화를 끊지 않고 다른 직원에게 물어본 뒤 다시 나에게 전달해 주는 방식이 됨.


### **[Hooks]**
> [Lifecycle Hooks Document](https://openai.github.io/openai-agents-python/ref/lifecycle/#agents.lifecycle.AgentHooks)


* **개념:** 특정 이벤트가 발생할 때 실행되는 리스너(Listener) 역할.
* **구독 방식:** 필요한 시점에 함수를 연결하여 사용할 수 있음.
* **시점:** 에이전트 호출 전(on_start)이나 호출 완료 후(on_end) 등에 실행됨.
* **용도:** 실시간 모니터링, 데이터 로깅, 상태 추적 등을 위해 필수적으로 사용됨.


### **[참고]**
* [Realtime Voice 관련 가이드](https://openai.github.io/openai-agents-python/voice/quickstart/)

