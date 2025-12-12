from crewai.flow.flow import Flow, listen, start, router, and_, or_
from pydantic import BaseModel

class MyFirstFlowState(BaseModel): # flow state 
    user_id : int = 1
    is_admin : bool = False 

class MyFirstFlow(Flow[MyFirstFlowState]): 

    @start()
    def first(self):
        print(self.state.user_id)
        print('Hello')

    @listen(first) # first라는 function의 종료를 listen한다. 
    def second(self):
        self.state.user_id = 2
        print('world')

    @listen(first)
    def third(self):
        print("!")

    #condition(조건)으로 listen도 가능 
    @listen(and_(second, third)) # second와 third가 끝나길 기다림 
    def final(self): 
        print(":)")

    @router(final)
    def route(self):
        a=2
        if self.state.is_admin:
            return 'even'
        else:
            return 'odd'

    @listen("even") # 이번에는 함수가 아닌 route함수의 이벤트를 listen함 
    def hadle_even(self):
        print("even")

    @listen("odd")
    def handle_odd(self):
        print("odd")

flow = MyFirstFlow()

flow.plot()
flow.kickoff()