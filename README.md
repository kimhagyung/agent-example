## AI Agents #10 Google ADK (Agent Development Kit)

### **[[ADK(Google ADK)](https://google.github.io/adk-docs/)]**

* CrewAI, AutoGen, OpenAI SDK, LangGraph 같은 기존 프레임워크들보다 가장 최근에 나온 따끈따끈한 도구
* Python뿐만 아니라 TypeScript, Go, Java까지 다양한 언어를 지원해서 확장성이 좋다 
* 다른 프레임워크들의 장점을 잘 섞어놓은 오케스트레이션(Orchestration) 프레임워크 느낌
* **멀티 에이전트 협업:** 복잡한 금융 상담 같은 업무를 여러 개의 전문 에이전트에게 나눠서 시키는 구조를 잡기 편하다
* **도구 활용(Tool Use):** 에이전트가 외부 API를 호출하거나 특정 함수를 실행하는 능력이 강력하다
* **개발자 환경 UI(Studio):** 개발 시 UI를 제공해줘서 Trace(추적), State(상태) 등을 시각적으로 확인하며 디버깅하기 용이하다
* **Gemini 최적화:** 구글에서 만든 만큼 제미나이(Gemini) 모델의 성능을 최대한 활용하고 연동하기 가장 좋음. (물론 OpenAI API 키를 연동해서 써도 상관없음)

### **[init.py]**

* 에이전트 폴더 하위에 `__init__.py`를 반드시 생성해 주어야 한다. 그래야 해당 폴더가 Python 패키지로 인식되고 진입점 역할을 하게된다
* `__init__.py` 파일 안에는 진입해야 할 에이전트를 `import` 하는 코드가 들어간다.
* 시스템이 이 파일에서 `root_agent`를 찾아 실행하는 구조라고 이해하면 된다(agent 파일에 root_agent 변수 필수)
* 
### **[sub_agents]**

메인 에이전트(Parent Agent)의 지시를 받아 복잡한 작업을 수행하는 전문화된 하위 AI 구성요소.

* **instruction:** 에이전트 자신의 페르소나와 작업 지침을 정의한다.
* **description:** 부모 에이전트가 이 서브 에이전트를 어떤 상황에 호출해야 하는지 설명. (OpenAI SDK의 `handoff`와 유사한 역할)

```python
# 하위 에이전트 정의
sub_agent = Agent(
    name="subAgent",
    instruction="You help with geo questions",
    description="Transfer to this agent when you have a geo related question"
)

# 부모 에이전트 정의 (하위 에이전트 등록)
parent_agent = Agent(
    name="parentAgent",
    instruction="You help the user with weather related questions",
    model=MODEL,
    sub_agents=[sub_agent]
)

```

### **[[State](https://adk-labs.github.io/adk-docs/ko/sessions/state)]**
에이전트가 대화 흐름을 기억하고 제어하기 위한 **공유 메모리**. Artifact보다 로직 구현에 있어 더 핵심적인 역할을 한다.

* **Context 유지:** 사용자의 이전 답변이나 추출된 정보를 저장하여 대화가 끊기지 않게 한다.
* **에이전트 간 협업:** 부모와 하위 에이전트가 동일한 `state` 객체를 공유하여 데이터를 주고받는다.
* **조건부 실행:** 저장된 상태값(예: `is_logged_in: True`)에 따라 에이전트의 다음 행동을 결정한다

### **[[Artifacts](https://google.github.io/adk-docs/artifacts/)]**

특정 상호작용 내에서 생성되거나 여러 세션에 걸쳐 지속되는 데이터 관리 기능.  <br> 
텍스트 이외의 데이터를 에이전트와 도구가 다룰 수 있도록 지원

* **멀티모달 데이터:** 오디오, 이미지, 영상 등의 파일을 저장하고 읽을 수 있다.
* **활용 예시:** 쇼츠 메이커와 같이 영상 파일을 생성하고 이를 에이전트가 참조하여 다음 작업을 수행해야 하는 경우에 사용.

### **[실행 방법]**

* [ADK](https://google.github.io/adk-docs/get-started/python/) 설치 후 아래 명령어 실행 (개발 환경 UI 실행)

```bash
adk web

```

### **[참고 사항]**

* **주의사항:** 이 UI는 개발 단계 전용이라 실제 상용(Production) 버전에서는 제공되지 않음.
* **참고:** 아직 자동 저장(Hot-reload) 기능은 없어서 코드를 수정할 때마다 서버를 재시작해 주어야 반영됨.

