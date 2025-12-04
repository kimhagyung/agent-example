.env 환경 파일 구성 

<img width="1085" height="509" alt="image" src="https://github.com/user-attachments/assets/21701be2-45cc-4c82-958f-1f10278d70ac" />



<br>
<b>OPENAI_API_KEY = "API_KEY" </b>  # openai(https://platform.openai.com/settings/organization/api-keys)에서 로그인 후  발급 <br>
<b>SERPER_API_KEY ="API_KEY"</b>   # serper(https://serper.dev)에서 계정 만든 후 무료api 키 발급<br>**


[실행방법]
터미널에 uv run main.py 입력 

[결과]
output 파일

[crewai 특징]
코드를 짜는 것 보다 프롬포트 쓰는데 더 시간이 들고 그래야 좋은 결과가 나온다. 

agent.yaml 파일의 "llm:" 부분에 원하는 모델을 넣을 수 있다. 모델은 아래 링크에서 선택 
https://platform.openai.com/docs/pricing 
