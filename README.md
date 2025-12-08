## AI Agents #4 CrewAI Job Hunter Agent

### **.env 환경 파일 구성** <br>

<img width="1289" height="145" alt="image" src="https://github.com/user-attachments/assets/f6d9c54d-b731-4575-9ff4-2a3f0879f05d" />

https://www.firecrawl.dev/app/playground?mode=search 에서 무료 api key 발급 받아 넣는다. <br><br>

### **[Firecrawl이란?]**

**Firecrawl**은 AI 에이전트 개발에 최적화된 웹 스크래핑 및 검색 도구이다.

* **주요 특징**:
    * 복잡한 웹페이지도 봇 차단 없이 스크래핑 가능하다.
    * 스크래핑한 데이터를 **Markdown**이나 **JSON** 등 LLM이 이해하기 쉬운 형식으로 자동 변환해 준다.
* **활용 (Search 모드)**:
    * 단일 페이지 스크래핑뿐만 아니라, 구글 검색처럼 키워드 검색(예: "Fullstack jobs in Denmark") 결과를 가져올 수 있다.
    * 검색된 각 페이지의 세부 콘텐츠까지 한 번에 가져와 주므로 별도의 2차 스크래핑 과정이 필요 없다. <br>

### <b>[실행방법]</b>
터미널에 **uv run main.py** 입력 

### <b>[결과]</b>
output 파일

### [CrewAI News Reader Agent 와의 차이] ###
이전 프로젝트(News Reader Agent)에서는 작업(Task)이 순차적(선형적)으로 진행되며, 앞 단계의 결과가 바로 뒷 단계로만 전달되었다. 
하지만 이번 Job Hunter Agent에서는 특정 Task가 바로 앞 단계뿐만 아니라, 이전의 여러 Task 결과값을 동시에 필요로 합니다. 이때 context 파라미터를 사용.

    @task
    def interview_prep_task(self):
        return Task(
            config=self.tasks_config["interview_prep_task"],
            context=[
                self.job_selection_task(),
                self.resume_rewriting_task(),
                self.company_research_task(),
            ],
        )
이런식으로 context = [] 로 받고 싶은 task를 선언 (CrewAI는 기본적으로 직전 Task의 결과를 전달하므로, 바로 앞 단계의 결과만 필요하다면 context를 명시할 필요가 없.)

### <b>models.py ###
pydantic 패키지를 사용해 데이터의 형태를 지정해준다. 
https://docs.pydantic.dev/latest/#pydantic-examples

### <b>참고</b>
Tool을 만들 때 firecrawl를 활용했는데 버전 업데이트로 강의 코드와 달라졌다. 
혹시 다음에도 버전이슈로 반환되는 데이터 객체의 구조가 달라질 수도있음. 


