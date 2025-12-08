from typing import List
from pydantic import BaseModel 
from datetime import date

class Job(BaseModel):
    # AI가일자리에 대해 어떤 정보를 넣길 원하는지 적(ex.직무, 위치, 재택여부)
    job_title: str
    company_name: str
    job_location: str
    is_remote_friendly: bool | None = None
    employment_type: str | None = None
    compensation: str | None = None
    job_posting_url: str
    job_summary: str

    key_qualifications: List[str] | None = None
    job_responsibilities: List[str] | None = None
    date_listed: date | None = None
    required_technologies: List[str] | None = None
    core_keywords: List[str] | None = None

    role_seniority_level: str | None = None
    years_of_experience_required: str | None = None
    minimum_education: str | None = None
    job_benefits: List[str] | None = None
    includes_equity: bool | None = None
    offers_visa_sponsorship: bool | None = None
    hiring_company_size: str | None = None
    hiring_industry: str | None = None
    source_listing_url: str | None = None
    full_raw_job_description: str | None = None


class JobList(BaseModel):
    # 여기서 JobList는 일자리목록이 포함된 리스트를 가지고 있다. 
     jobs: List[Job] 

class RankedJob(BaseModel):  # job_matching_task의 반환형식
    job: Job # job은 그대로 
    match_score : int 
    reason : str

class RankedJobList(BaseModel):
    ranked_jobs : List[RankedJob] #우선순위가 매겨진 직무 리스트 

class ChosenJob(BaseModel):  # tasks.yaml 에 job_selection_task 참고 
    job : Job 
    selected : bool #직무 선택 여부 
    reason : str