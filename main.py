from crewai.flow.flow import Flow, listen, start, router, and_, or_
from pydantic import BaseModel

# flow는 그저 class이다. 
# flow는 여러개의 method를 가진 class임 
# 위에 listen, start, router, and_, or_ 이 것들을 flow(class) 내의 method들을 언제 실행시켜 줄 지 데코레이터 지정해줌 

# or_ : 여러개의 function을 listen(감지, 수신)할 수 있다. 그 중 하나가 끝나면 코드가 실행되게 할 수 있다. 
# and_ : 여러 function을 listen할 수 있다. 이건 모든 function이 끝나야만 코드를 실행할 수 있다. 
    
class ContentPipelineState(BaseModel):

    # inputs
    content_type : str=""
    topic: str=""

    # Internal
    max_length : int = 0

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
        print('Researching...')
        return True

    @router(conduct_research)
    def router(self):
        content_type = self.state.content_type

        if content_type == "blog":
            return "make_blog"
        elif content_type == "tweet":
            return "make_tweet"
        else:
            return "make_linkedin_post"

    @listen("make_blog")   #각 변수에 대한 리스너 
    def handle_make_blog(self):
        print("Making blog post...")

    @listen("make_tweet")    
    def handle_make_tweet(self):
        print("Making tweet...")

    @listen("make_linkedin_post")    
    def handle_make_linkedin_post(self):
        print("Making linkedin post...")

    @listen("handle_make_blog")    
    def check_seo(self):
        print("Checking log SEO..")
    
    @listen(or_(handle_make_tweet, handle_make_linkedin_post))
    def check_virality(self):
        print("Checking virality...")

    @listen(or_(check_virality, check_seo))
    def finalize_content(self):
        print("Finalizing content")



flow = ContentPipelineFlow()


# flow.kickoff(
#     inputs={
#         "content_type" : "tweet",
#         "topic" : "AI Dog Training",
#     }
# )

flow.plot()