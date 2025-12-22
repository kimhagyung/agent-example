## AI Agents  #6 Autogen Grok Deep Research Agent

### **[.env 환경 파일 구성]** <br>
이전과 동일 <br>

### **[목표]** <br>
여러 에이전트를 하나의 그룹 채팅에 넣어 서로 협업·토론하며(사람 개입 포함) 작업을 완료하는 멀티에이전트 대화형 애플리케이션을 만든다. 

### <b>[결과]</b>
email-optimizer-team.ipynb > 파일자체  <br>
deep-research-team.ipynb > report.md

### **Autogen 특징**
https://microsoft.github.io/autogen/stable/
* Microsoft에서 개발한 멀티 에이전트 프레임워크
* 출시된 지 오래되어 최신 트렌드 대비 다소 구식한 인상
* High-level abstraction이 많아 깊게 사용하려면 개념 학습 비용이 큼
* 멀티 에이전트 프레임워크 중 드물게 .NET 지원 제공

### **[Autogen Teams]** <br>
https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html
<img width="679" height="302" alt="image" src="https://github.com/user-attachments/assets/71766827-ec2b-4e88-b784-8787a326b490" />

[4개의 Team이 존재하며 해당 코드는 RoundRobinGroupChat, SelectorGroupChat 만 다룬다.]
 
#### **[Team - RoundRobinGroupChat ]** <br>
* 그룹챗을 참가자들의 순서를 round-robin 방식으로 운영하는 팀
* round robin 끝에 도달하면 마지막 ai가 평가 후 재생성 or 끝을 정함

 #### **[Team - SelectorGroupChat ]** <br>
* 여러 agent가 **하나의 그룹 챗(conversation history 공유)**에 참여
* **누가 발화할지 결정하는 전용 selector AI**가 존재
* selector는 **대화 히스토리와 현재 task를 기반**으로 다음 speaker를 선택
* 발화 선택 자체가 **하나의 독립된 AI task**로 동작
* **ChatCompletionModel을 사용해 다음 speaker를 고르는 팀 구조**

→ 모든 agent는 동일한 대화 맥락을 공유하지만, 실제 발화 순서는 selector AI가 동적으로 결정하는 구조

### **[참고]** <br>
결과가 한글로 나왔으면 하는 마음에 강의영상을 보며 한글로 번역하여 작성했지만 모델 성능이슈인지 잘 되지는 않았다.
결과적으로 Autogen을 실제 프로젝트에 사용할 가능성이 낮다고 판단하여, 추가 개선은 진행하지 않았다 (API 비용 이슈 포함).



