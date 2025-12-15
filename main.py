from typing import List
from crewai.flow.flow import Flow, listen, start, router, and_, or_
from crewai import Agent 
from crewai import LLM
from pydantic import BaseModel
from urllib3 import response
from tools import web_search_tool
from seo_crew import SeoCrew

# flow는 그저 class이다. 
# flow는 여러개의 method를 가진 class임 
# 위에 listen, start, router, and_, or_ 이 것들을 flow(class) 내의 method들을 언제 실행시켜 줄 지 데코레이터 지정해줌 

# or_ : 여러개의 function을 listen(감지, 수신)할 수 있다. 그 중 하나가 끝나면 코드가 실행되게 할 수 있다. 
# and_ : 여러 function을 listen할 수 있다. 이건 모든 function이 끝나야만 코드를 실행할 수 있다. 

# output 들 정의 
class BlogPost(BaseModel):
    title: str
    subtitle: str
    sections: List[str]


class Tweet(BaseModel):
    content: str
    hashtags: str


class LinkedInPost(BaseModel):
    hook: str
    content: str
    call_to_action: str


class Score(BaseModel):

    score: int = 0
    reason: str = ""


class ContentPipelineState(BaseModel):

    # inputs
    content_type : str=""
    topic: str=""

    # Internal
    max_length : int = 0 
    research : str=""
    score: Score | None = None

    # Content
    blog_post: BlogPost | None = None # 기본값도 None
    tweet: Tweet | None = None
    linkedin_post: LinkedInPost | None = None

class ContentPipelineFlow(Flow[ContentPipelineState]):

    @start()
    def init_content_pipeline(self):   #state를 검증하는 
        if self.state.content_type not in ["tweet", "blog", "linkedin"]:
            raise ValueError("The content type is wrong")    

        if self.state.topic  == "":
            raise ValueError("The topic can't be blank.")

        if self.state.content_type == "tweet":
            self.state.max_length = 150
        elif self.state.content_type == "blog":
            self.state.max_length  = 800
        elif self.state.content_type == "linkedin":
            self.state.max_length = 500
        
    @listen(init_content_pipeline)
    def conduct_research(self):  # 위의 값에 대해 ? 조사중인 함수 (리서치크루)
        researcher = Agent(
            role="수석 연구원",
            backstory="당신은 흥미로운 사실과 통찰력을 발굴하는 것을 즐기는 디지털 탐정입니다. 남들이 놓치는 알짜배기 정보를 찾아내는 탁월한 감각을 가지고 있습니다.",
            goal=f"{self.state.topic}에 관해 가장 흥미롭고 유용한 정보를 찾아내세요.",
            tools=[web_search_tool],
        )

        self.state.research = researcher.kickoff(f"{self.state.topic}에 관해 가장 흥미롭고 유용한 정보를 찾아내세요.")
    
    @router(conduct_research)
    def conduct_research_router(self):
        content_type = self.state.content_type

        if content_type == "blog":
            return "make_blog"
        elif content_type == "tweet":
            return "make_tweet"
        else:
            return "make_linkedin_post"

    @listen(or_("make_blog", "remake_blog"))   #각 변수에 대한 리스너 
    def handle_make_blog(self):
        blog_post = self.state.blog_post

        llm = LLM(model="openai/o4-mini", response_format=BlogPost)

       
        if blog_post is None:
            # [수정됨] 블로그 생성 프롬프트 (한국어)
            result = llm.call(
                f"""
                주제 '{self.state.topic}'에 대한 좋은 SEO를 가지는 블로그 포스트를 작성해 주세요.
                반드시 아래의 조사 자료를 바탕으로 작성해야 하며, 언어는 **한국어**입니다.

                <research>
                ================
                {self.state.research}
                ================
                </research>
                """
            )
        else:
            # [수정됨] 블로그 수정(Refine) 프롬프트 (한국어)
            result = llm.call(
                f"""
                당신이 '{self.state.topic}'에 대해 작성한 블로그 글이 SEO 점수가 낮습니다.
                
                이유: {self.state.score.reason}
                
                위 내용을 반영하여 글을 개선해 주세요.
                아래의 조사 자료를 다시 참고하고, 반드시 **한국어**로 작성하세요.

                <blog post>
                {self.state.blog_post.model_dump_json()}
                </blog post>

                <research>
                ================
                {self.state.research}
                ================
                </research>
                """
            )

        self.state.blog_post = result

    @listen(or_("make_tweet","remake_tweet"))    
    def handle_make_tweet(self):

        tweet = self.state.tweet

        llm = LLM(model="openai/o4-mini", response_format=Tweet)

       
        if tweet is None:
            # [수정됨] 블로그 생성 프롬프트 (한국어)
            result = llm.call(
                f"""
                주제 '{self.state.topic}'로 바이럴 될 만한 tweet을 작성해 주세요.
                반드시 아래의 조사 자료를 바탕으로 작성해야 하며, 언어는 **한국어**입니다.

                <research>
                ================
                {self.state.research}
                ================
                </research>
                """
            )
        else:
            # [수정됨] 블로그 수정(Refine) 프롬프트 (한국어)
            result = llm.call(
                f"""
                당신이 '{self.state.topic}'에 대해 작성한 tweet이 SEO 점수가 낮습니다.
                
                이유: {self.state.score.reason}
                
                위 내용을 반영하여 글을 개선해 주세요.
                아래의 조사 자료를 다시 참고하고, 반드시 **한국어**로 작성하세요.

                <tweet>
                {self.state.tweet.model_dump_json()}
                </tweet>

                <research>
                ================
                {self.state.research}
                ================
                </research>
                """
            )
        self.state.tweet = result


    @listen(or_("make_linkedin_post","remake_linkedin_post"))    
    def handle_make_linkedin_post(self):
        
        linkedin_post = self.state.tweet

        llm = LLM(model="openai/o4-mini", response_format=LinkedInPost)

       
        if linkedin_post is None:
            # [수정됨] 블로그 생성 프롬프트 (한국어)
            result = llm.call(
                f"""
                주제 '{self.state.topic}' 로 바이럴 될 만한 linkedin post를 작성해  주세요.
                반드시 아래의 조사 자료를 바탕으로 작성해야 하며, 언어는 **한국어**입니다.

                <research>
                ================
                {self.state.research}
                ================
                </research>
                """
            )
        else:
            # [수정됨] 블로그 수정(Refine) 프롬프트 (한국어)
            result = llm.call(
                f"""
                당신이 '{self.state.topic}'에 대해 작성한 linkedin post이 SEO 점수가 낮습니다.
                
                이유: {self.state.score.reason}
                
                위 내용을 반영하여 글을 개선해 주세요.
                아래의 조사 자료를 다시 참고하고, 반드시 **한국어**로 작성하세요.

                <linkedin_post>
                {self.state.linkedin_post.model_dump_json()}
                </linkedin_post>

                <research>
                ================
                {self.state.research}
                ================
                </research>
                """
            )
        self.state.linkedin_post =result


    @listen("handle_make_blog")    
    def check_seo(self):

        result = SeoCrew().crew().kickoff(  # SEO 팀, 지금 작성된 글 좀 평가해 줘! 라는 부분 
            {
                "topic":self.state.topic,
                "blog_post": self.state.blog_post.model_dump_json()   # 작성된 글을 전달
            }
        )
        self.state.score = result.pydantic # crew의 결과값의 pydantic에 접근하면 출력값에 접근가능 
    
    @listen(or_(handle_make_tweet, handle_make_linkedin_post))
    def check_virality(self):
        print(self.state.tweet)
        print(self.state.linkedin_post)
        print("Checking virality...")

    @router(or_(check_seo, check_virality))
    def score_router(self):
        content_type = self.state.content_type
        score = self.state.score
        print("score :",score)
        
        if score.score >= 8:
            return "check_passed"
        else:
            if content_type == "blog":
                return "remake_blog"
            elif content_type == "linkedin":
                return "remake_linkedin_post"
            else:
                return "remake_tweet"
                

    @listen("check_passed")
    def finalize_content(self):
        print("Finalizing content")



flow = ContentPipelineFlow()


flow.kickoff(
    inputs={
        "content_type" : "blog",
        "topic" : "AI를 활용한 강아지 훈련법",
    }
)

#flow.plot()