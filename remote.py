import vertexai
from vertexai import agent_engines 

PROJECT_ID = "gen-lang-client-0425685729"
LOCATION = "asia-northeast1" # 서버를 두고싶은 위치 
BUCKET = "gs://nico-weather_agent"  #나의 구글 클라우드 스토리지 버킷 이름  

vertexai.init(
    project = PROJECT_ID,
    location = LOCATION,
)

# 1.배포 가져오기 
# deployments = agent_engines.list()

# for deployment in deployments:
#     print(deployment)

DEPLOYMENT_ID = "projects/57920741189/locations/asia-northeast1/reasoningEngines/1979974151019954176"
SESSION_ID = "1622523470585790464"

remote_app = agent_engines.get(DEPLOYMENT_ID)

# remote_app.delete(force=True) # 이러면 삭제가능

print(remote_app.display_name)

# 세션 id 얻기위함
# remote_session = remote_app.create_session(user_id="u_123")

# print(remote_session['id'])

# 
for event in remote_app.stream_query(
    user_id="u_123", 
    session_id = SESSION_ID, 
    message = "I'm going to Laos, any tips?"
):
    print(event, "\n","="*50)