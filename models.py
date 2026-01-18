from pydantic import BaseModel 

# 유저 계정 context를 위한 BaseModel 생성 
class UserAccountContext(BaseModel):
    #여기는 가상의 데이터 넣을거임 
    customer_id : int
    name : str
    tier: str = "basic" # 티어는 외에도 premium, entreprise 등등 있을거임

