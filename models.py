from pydantic import BaseModel 

# 유저 계정 context를 위한 BaseModel 생성 
class UserAccountContext(BaseModel):
    #여기는 가상의 데이터 넣을거임 
    customer_id : int
    name : str
    tier: str = "basic" # 티어는 외에도 premium, entreprise 등등 있을거임
    email : str = "nico@co.kr"

class InputGuardRailOutput(BaseModel):
    is_off_topic : bool 
    reason : str # 이거 도와줄 수 없어 ~ 이 이유 때문에 

class TechnicalOutputGuardRailOutput(BaseModel):
    contains_off_topic : bool # 다른종류의 데이터 포함 여부 
    contains_billing_data : bool # technical agent가 요금 관련 질문 하면 여기서 캐치함
    contains_accouts_data : bool  
    reason : str 


class HandoffData(BaseModel):

    to_agent_name: str
    issue_type: str
    issue_description: str
    reason: str
    