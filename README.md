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

한마디로 **"중앙 집중식 명령 체계"**가 핵심인 구조.

* **Supervisor(관리자)의 역할**:
* 유저와 직접 소통하는 유일한 접점(위 그림에서 색칠된 노드).
* 일종의 **스마트한 라우터** 역할을 수행함. 유저의 요청을 분석해서 가장 잘 처리할 수 있는 하위 에이전트에게 일을 시킴.


* **작동 방식**:
* **양방향 커뮤니케이션**: 하위 에이전트들은 유저에게 직접 답하지 않고, 작업 결과를 무조건 **Supervisor에게 반환**.
* Supervisor는 응답을 보고 "일이 끝났는지" 혹은 "다음 에이전트에게 또 시킬 일이 있는지" 판단.


* **장점**: 유저가 복잡하고 큰 요청을 보내도 Supervisor가 단계별로 에이전트들을 부려가며 체계적으로 결과를 만들어낸다.

---

**아키텍처별 차이점이 명확하게 보이지? 다음 섹션인 "Supervisor as Tools" 방식까지 추가로 정리해 줄까?**
