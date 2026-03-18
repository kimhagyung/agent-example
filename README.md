# #16: AI Agents - Workflow Architectures
---

### 환경 설정

* **.env 환경 파일 구성**: 이전 섹션과 동일한 구성을 사용

### 학습 목표

* 다양한 워크플로우 아키텍처의 개념을 습득하고 구현 능력을 배양 
* **참고 자료**: [Anthropic - Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)

---

### Prompt Chaining (프롬프트 연결 기법)
<img width="852" height="362" alt="image" src="https://github.com/user-attachments/assets/f4c50614-4208-4470-91c4-6cca21314c68" />

**Prompt Chaining**은 하나의 복잡한 작업을 여러 단계의 순서로 세분화하여 처리하는 방식 

* **동작 원리**: 각 LLM 호출 단계의 출력이 다음 단계의 입력으로 전달되어 순차적으로 처리 
* **제어 방법**: 개발자의 의도에 따라 단계 사이에 프로그램적 검증인 **게이트(Gate)**를 추가할 수 있다. 특정 조건을 코딩하여 이를 통과할 경우에만 흐름을 계속 이어가도록 설계 

---

### Gates (검증 단계)

**Gate**는 전체 프로세스가 의도한 방향으로 잘 진행되고 있는지 확인하는 품질 관리 지점.

* **역할**: 워크플로우 중간에서 프로세스의 상태와 출력값의 품질을 점검 
* **주요 기능**:
    * **품질 필터링**: LLM의 답변이 기준 미달이거나 형식이 잘못된 경우 다음 단계로 넘어가지 않도록 차단 
    * **흐름 제어**: 검증 결과에 따라 프로세스를 즉시 종료하거나, 수정을 위해 이전 단계로 되돌리는 등 유연한 흐름생성
* **결과 처리**: 위 그래프 구성에 따르면, 검증을 통과하지 못할 경우 프로세스는 그대로 종료되거나 의도된 루프/이탈 경로를 탄다

---

### Routing Architecture
<img width="843" height="358" alt="image" src="https://github.com/user-attachments/assets/9d1612ee-1199-4d0c-ab12-ef0cba9f3b17" />

라우팅은 입력을 분류하고 특화된 후속 작업으로 연결. 이러한 워크플로를 통해 관심사를 분리하고 더욱 세분화된 프롬프트를 구축할 수 있습니다. 이 워크플로가 없으면 특정 유형의 입력에 최적화하는 것이 다른 입력의 성능을 저하시킬 수있다.

* **사용 시기**: 명확하게 구분된 범주가 있어 각각 별도로 처리하는 것이 더 나은 복잡한 작업에 적합하며, LLM이나 분류 알고리즘을 통해 정확하게 분류할 수 있는 경우 효과적 
* **활용 예시**:
    * **고객 서비스**: 일반 질문, 환불 요청, 기술 지원을 각각의 전용 하위 프로세스로 연결
    * **모델 최적화**: 쉬운 질문은 가성비 좋은 모델(Haiku)로, 어려운 질문은 고성능 모델(Sonnet)로 배분

---

### Parallelization Architecture (병렬화)
<img width="860" height="356" alt="image" src="https://github.com/user-attachments/assets/13c1e62c-b944-4e59-9f9c-ce57d360a560" />

여러 노드를 동시에 병렬로 실행하는 방식  

1. **분할(Sectioning)**: 이전 노드의 값을 받지 않고 독립적인 노드들을 동시에 실행
2. **투표(Voting)**: 동일한 작업을 여러 번 실행한 뒤, **집계(Aggregator)** 노드에서 최적의 결과 선택

* **사용 시기**: 하위 작업을 병렬로 돌려 속도를 높여야 할 때, 혹은 여러 관점의 시도가 필요하여 결과의 신뢰도를 높여야 할 때 사용 
* **활용 예시**:
    * **가드레일**: 응답 생성과 동시에 부적절한 콘텐츠를 걸러내는 인스턴스를 병렬 실행
    * **코드 검토**: 여러 프롬프트가 코드를 동시 검토하여 취약점 플래그 지정

---

### Orchestrator-workers Architecture
<img width="856" height="350" alt="image" src="https://github.com/user-attachments/assets/538b6e1f-093b-4e02-a5da-d98e8559cd9b" />

Parallel workflow와 비슷해 보이지만, 앞단에 **Orchestrator** 노드가 있다는 점이 핵심 .

* **동적 작업 할당**: Parallel은 노드 개수와 연결(Edge)이 미리 정의되어 있지만, 이 구조는 Orchestrator가 실행 시점에 워커가 몇 명이나 필요할지 직접 결정 
* **유연성**: LangGraph의 `send` 커맨드 등을 통해 노드를 동적으로 생성할 수 있으며, LLM이 작업을 스스로 분해하여 처리 
* **특징**: 모든 task를 미리 정의하기 어려운 복잡하고 가변적인 작업에 적합 
