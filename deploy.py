import dotenv 
dotenv.load_dotenv()
import os 
import vertexai
import vertexai.agent_engines 
from travel_advisor_agent.agent import travel_advisor_agent
from vertexai.preview import reasoning_engines


PROJECT_ID = "gen-lang-client-0425685729"
LOCATION = "asia-northeast1" # 서버를 두고싶은 위치 
BUCKET = "gs://nico-weather_agent"  #나의 구글 클라우드 스토리지 버킷 이름  

vertexai.init(
    project = PROJECT_ID,
    location = LOCATION,
    staging_bucket = BUCKET,
)

app = reasoning_engines.AdkApp(
    agent = travel_advisor_agent , 
    enable_tracing = True, # 어드민에서 trace를 보여주기 위해 
)

# 구글 클라우드 서비스인 agent engine안에 agent를 생성 
remote_app = vertexai.agent_engines.create(
    display_name = "Travel Advisor Agent",
    agent_engine =  app, 
    requirements = [ # agent를 실행하기 위해 필요한 의존성 ㅈ
        "google-cloud-aiplatform[adk, agent_engines]",
        "litellm", 
    ], 
    extra_packages=[ # agent를 실행하는데 필요한 모든 폴더들(travel_advisor_agent 폴더임 ㅇㅇ) 
        "travel_advisor_agent"
    ],
    env_vars={
        "OPENAI_API_KEY":os.environ.get("OPENAI_API_KEY")
    }
)