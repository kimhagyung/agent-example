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

### **[실행 방법]**

* [ADK](https://google.github.io/adk-docs/get-started/python/) 설치 후 아래 명령어 실행 (개발 환경 UI 실행)

```bash
adk web

```

### **[참고 사항]**

* **주의사항:** 이 UI는 개발 단계 전용이라 실제 상용(Production) 버전에서는 제공되지 않음.
* **참고:** 아직 자동 저장(Hot-reload) 기능은 없어서 코드를 수정할 때마다 서버를 재시작해 주어야 반영됨.
