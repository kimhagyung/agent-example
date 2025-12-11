from crewai.flow.flow import Flow, listen, start, router, and_, or_

# flow는 그저 class이다. 
# flow는 여러개의 method를 가진 class임 
# 위에 listen, start, router, and_, or_ 이 것들을 flow(class) 내의 method들을 언제 실행시켜 줄 지 데코레이터 지정해줌 

# or_ : 여러개의 function을 listen(감지, 수신)할 수 있다. 그 중 하나가 끝나면 코드가 실행되게 할 수 있다. 
# and_ : 여러 function을 listen할 수 있다. 이건 모든 function이 끝나야만 코드를 실행할 수 있다. 

class MyFirstFlow(Flow):

    @start()
    def first(self):
        print('Hello')

    @listen(first) # first라는 function의 종료를 listen한다. 
    def second(self):
        print('world')

    @listen(first)
    def third(self):
        print("!")

    #condition(조건)으로 listen도 가능 
    @listen(and_(second, third)) # second와 third가 끝나길 기다림 
    def final(self):
        print(":)")

flow = MyFirstFlow()

flow.plot() # 도식화 