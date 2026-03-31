## AI Agents #18 Multi Agent Architectures

### **.env 환경 파일 구성**

* 이전 섹션과 동일한 설정을 사용함.

### **학습 목표**

다양한 **멀티 에이전트 아키텍처(Multi-Agent Architectures)**의 종류와 특징을 이해한다.

* **Network, Supervisor, Supervisor as Tools** 아키텍처의 구조와 차이점 습득

---

### **1. Network Architecture**
 <img width="213" height="227" alt="image" src="https://github.com/user-attachments/assets/c917db20-1bbc-43a0-97c8-25ee0fe0a899" />

여러 개의 에이전트가 **계층 구조 없이 수평적으로 연결**되어 서로 소통하는 방식.

* **특징**: 모든 에이전트가 대화의 통제권을 다른 에이전트에게 넘길 수 있는 권한을 가진다.
* **구조**: 각각의 에이전트(사각형)는 내부에 `Start`, `LLM 노드`, `Tool 노드`, `End 노드`를 가진 독립적인 그래프
* **구현 포인트**:
* 핵심은 에이전트를 생성하는 공통 함수(`make_agent` 등)를 만드는 것.
* 이 함수를 필요한 만큼(예: 4번) 호출하여 각각의 그래프를 가진 에이전트들을 생성하고 서로 연결함.
* 모두가 대등한 관계에서 통제권을 주고받으며 협력하는 구조.
---

### **2. Supervisor Architecture**

<img width="221" height="248" alt="image" src="https://github.com/user-attachments/assets/153d9136-bb3c-45cc-bfd0-2fe402c5655a" />

**중앙 집중식 명령 체계**가 핵심인 구조이다. 

* **Supervisor(관리자)의 역할**:
* 유저와 직접 소통하는 유일한 접점(위 그림에서 색칠된 노드).
* 일종의 **스마트한 라우터** 역할을 수행함. 유저의 요청을 분석해서 가장 잘 처리할 수 있는 하위 에이전트에게 일을 시킴.


* **작동 방식**:
* **양방향 커뮤니케이션**: 하위 에이전트들은 유저에게 직접 답하지 않고, 작업 결과를 무조건 **Supervisor에게 반환**.
* Supervisor는 응답을 보고 "일이 끝났는지" 혹은 "다음 에이전트에게 또 시킬 일이 있는지" 판단.


* **장점**: 유저가 복잡하고 큰 요청을 보내도 Supervisor가 단계별로 에이전트들을 부려가며 체계적으로 결과를 만들어낸다.

--- 

### **3. Supervisor as Tools**

 <img width="279" height="350" alt="image" src="https://github.com/user-attachments/assets/16ba671e-e467-4b92-b717-6882d70519d2" />

Supervisor 아키텍처와 유사하지만, 하위 에이전트들을 **'노드'가 아닌 '도구(Tool)'로 취급**하여 호출하는 방식이다.

  * **핵심 차이점**:
      * **Supervisor**: `Command`를 통해 제어권(Control) 자체를 하위 노드로 완전히 넘겼다가 다시 돌려받는 방식.
      * **Supervisor as Tools**: Supervisor 노드가 하위 에이전트를 단순히 하나의 **Tool로서 호출**함. 제어권은 여전히 Supervisor가 쥐고 있으며, 에이전트의 실행 결과(응답)만 리턴받아 활용한다.
  * **구조적 특징**:
      * 여러 개의 도구를 가진 하나의 거대한 Supervisor 노드를 구축하는 형태.
      * 이때 도구(Tool)는 단순한 함수일 수도 있고, 독립적인 **Sub-graph**나 **LangGraph Agent**가 될 수도 있다.
  * **장점**: 제어 흐름이 끊기지 않고 하나의 노드에서 관리되므로, 복잡한 상태 관리가 비교적 직관적이다.

-----

### **4. Prebuilt Agents & Hierarchical**

<img width="421" height="482" alt="image" src="https://github.com/user-attachments/assets/45bf1df8-bd0c-4819-b2d8-56dff0a6e412" />

계층적 구조(Hierarchical)는 앞서 배운 Supervisor 패턴을 중첩하여 반복하는 구조이므로 별도의 구현은 생략 

  * **LangGraph Prebuilt**:
      * 지금까지 우리가 직접 설계하고 연결했던 복잡한 에이전트 구조들은 사실 LangGraph에서 상당 부분 **미리 구현(Prebuilt)** 하여 제공하고 있다.
      * `create_react_agent`와 같은 내장 함수를 활용하면, 반복적인 그래프 설계 없이도 검증된 아키텍처를 빠르게 도입할 수 있다.
      * [LangGraph API Reference](https://langchain-ai.github.io/langgraph/reference/prebuilt/) (최신 문서 링크 참고) 
