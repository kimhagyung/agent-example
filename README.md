## AI Agents #3 CrewAI News Reader Agent

### **.env 환경 파일 구성**

<img width="1085" height="509" alt="image" src="https://github.com/user-attachments/assets/033f7a65-b476-4a93-b008-7786d31019f4" />

<br>
<b>OPENAI_API_KEY = "API_KEY" </b>  # openai(https://platform.openai.com/settings/organization/api-keys)에서 로그인 후  발급 <br>
<b>SERPER_API_KEY ="API_KEY"</b>   # serper(https://serper.dev)에서 계정 만든 후 무료api 키 발급<br><br>


### <b>[실행방법]</b>
터미널에 uv run main.py 입력 

### <b>[결과]</b>
output 파일

### <b>[crewai 특징]</b>
1. 초보 친화적 프레임워크
2. 유저를 위해 알아서 해주는게 많음
3. 세세하게 컨트롤한 커스터마이징 <b>불가능</b>
4. 코드를 짜는 것 보다 프롬포트 쓰는데 더 시간이 들고 그래야 좋은 결과가 나옴.<br>

### <b>참고</b>
agent.yaml 파일의 "llm:" 부분에 원하는 모델을 넣을 수 있다. 모델은 아래 링크에서 선택 
https://platform.openai.com/docs/pricing 
