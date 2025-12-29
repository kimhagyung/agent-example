## AI Agents #7 Introducing OpenAI Agents SDK & AI Agents #8 OpenAI Agents SDK: ChatGPT Clone

### **[.env 환경 파일 구성]**

이전과 동일

### **[목표]**

Streamlit을 사용하여 파이썬 UI를 생성하고, **OpenAI Agents SDK**를 활용해 여러 개의 MCP 서버와 Tool을 탑재한 ChatBot(ChatGPT-clone)을 만든다.

### **[OpenAI Agents SDK]**

* **URL:** [https://openai.github.io/openai-agents-python/](https://openai.github.io/openai-agents-python/)
* **특징:** 매우 가볍고, 새로 배워야 할 복잡한 개념이 거의 없다.
* **장점:** 사용하기 쉽고 **Abstraction(추상화)**이 거의 없다. (즉, 완성된 장난감이 아니라 '레고 블록' 자체를 우리에게 준다는 뜻. 조립은 우리가 한다.)

### **[Abstraction(추상화)이란?]**

#### **높은 추상화 (예: CrewAI 등):**

* 누군가가 레고 블록을 가져가서 우리를 위해 **완성된 성**을 조립해 주고 나서 "자, 이거 갖고 놀아" 하고 주는 것과 같다.
* 당장은 편하지만, 성 문을 다른 곳에 달고 싶거나 구조를 바꾸려 하면 뜯어고치기가 엄청 힘들다. (내부 로직이 숨겨져 있어서 커스터마이징이 어려움)

#### **낮은 추상화 (OpenAI Agents SDK):**

* 완성품이 아니라 **레고 블록(부품)** 봉지를 뜯어서 우리한테 주는 것과 같다.
* "성은 네가 쌓고 싶은 대로 쌓아."라는 식이라 투명하고 자유도가 매우 높다.

#### **Agent SDK에서 제공하는 Primitives(기본 요소)**

우리가 조립해야 할 '레고 블록'들은 딱 아래와 같으며, 복잡한 마법 없이 아주 직관적이다.

1. **Agent (주체):**
* "너는 챗봇이야", "너는 코딩 도우미야"라고 이름과 역할(System Prompt)만 정해주는 껍데기.


2. **Tools (도구):**
* 에이전트 손에 쥐여주는 기능들. (예: `web_search()`, `get_weather()` 같은 파이썬 함수).
* "모르면 이거 써서 찾아봐"라고 쥐여주는 도구상자.


3. **Handoff (연결/토스):**
* **핵심 기능!** "이거 내가 해결 못 하면 **B 에이전트한테 넘겨(Transfer)**"라고 명시하는 것.
* 복잡한 로직을 짤 때, 에이전트끼리 공 던지기 하듯 대화를 넘기는 흐름을 우리가 직접 연결한다.


4. **Guardrails (안전장치):**
* "이런 말은 하지 마", "입력값은 이 포맷이어야 해"라고 체크하는 검문소.


5. **Session (대화 맥락):**
* 대화 내용을 담는 **그릇**이다.
* 에이전트가 방금 한 말을 까먹지 않고 기억하게 해주는 저장소. 대화가 끊기지 않고 이어지게(Multi-turn) 해주는 필수 요소다. (이게 없으면 에이전트는 붕어 기억력이 됨)



**결론:**
이런 기본적인 요소(블록)들만 던져주고, **"누가 누구한테 말을 걸고, 언제 도구를 쓸지는 네가 파이썬 코드로 직접 짜"**는 것이다.
그래서 코드가 매우 직관적이고 디버깅하기 좋다.

#### **[공식문서]**

<img width="1019" height="470" alt="image" src="https://github.com/user-attachments/assets/1338eb9d-0e22-4b90-96a1-cf57db738c8c" />

#### **[한글번역]**

<img width="1008" height="437" alt="image" src="https://github.com/user-attachments/assets/2633a893-1f43-4428-be8b-c260142fc5e1" />

### **[Tracing(추적) 기능이란?]**

확인 경로: [https://platform.openai.com/logs?api=chat-traces](https://platform.openai.com/logs?api=chat-traces)

#### **[정의]**

* Agents SDK로 만든 에이전트가 수행하는 **모든 일거수일투족**을 의미한다.
* 단순 텍스트 로그뿐만 아니라, OpenAI 대시보드(Dashboard)에서 시각화된 데이터로 볼 수 있으며, **어떤 Tool을 호출했는지(Tool Call)**까지 전부 확인 가능하다.

#### **[기존 프레임워크 (CrewAI, AutoGen 등)의 문제점]**

* **"기도 메타 (Pray and Hope)":** 에이전트를 실행시키고 나서 "제발 에러 없이 잘 돌아가라..." 하고 기도하는 것밖에 못 한다.
* **답답한 시야:** 우리가 볼 수 있는 건 콘솔 창에 찍히는 텍스트 로그뿐. 스크롤만 하염없이 내리면서 확인해야 한다.
* **제어권 부족:** 실제로 Tool을 실행하는 데 **시간이 얼마나 걸렸는지**, 정확히 **어떤 Tool이 어떻게 호출됐는지** 디테일하게 추적하거나 통제하기가 어렵다.

#### **[OpenAI Agents SDK의 차별점]**

* **기본 활성화 (Built-in):** 복잡한 설정 없이 Tracing 기능이 **기본적으로 켜져 있다(Default On)**.
* **강력한 시각화:** 에이전트를 호출할 때마다 **OpenAI 대시보드**에 자동으로 로그가 남는다.
* **투명성:** "아, 여기서 이 툴을 썼구나", "여기서 시간이 오래 걸렸구나"를 눈으로 보고 확실하게 파악이 가능하다.

#### **[dummy-agent.ipynb]**

최종 결과물에는 포함되지 않으며, 일단 챗봇 기능만 테스트하기 위해 구현한 코드이다.

#### **[Session Memory]**

`SQLiteSession`을 import 하여 세션을 DB에 저장함으로써 대화 기억(Memory)을 유지할 수 있다. (추후 Runner에 추가 예정)

```python
# 사용 예시
# SQLiteSession(세션_식별자, DB_파일_경로)
session = SQLiteSession("user_1", "ai-memory.db") 

# 세션 초기화 (대화 내용 삭제)
await session.clear_session()

```

참고로 SQLiteSession이 아닌 다른 DB나 서버, 회사 API를 사용하고 싶다면 아래 문서를 참고하면 된다.
[Custom Memory Implementations 문서](https://openai.github.io/openai-agents-python/sessions/#custom-memory-implementations)

#### **[Streamlit]**

**[참고문서]**
[https://docs.streamlit.io/develop/api-reference](https://docs.streamlit.io/develop/api-reference)

**[실행방법]**

```bash
streamlit run main.py

```

