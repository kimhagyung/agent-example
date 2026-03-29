from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import START, END, StateGraph, MessagesState
from agent.classification_agent import classification_agent
from agent.teacher_agent import teacher_agent
from agent.feynman_agent import feynman_agent

class TutorState(MessagesState):
    current_agent : str # 다른 에이전트로 전환될떄마다, 그걸 state에 저장하는 용도임. 

def router_check(state : TutorState):
    current_agent = state.get("current_agent", "classification_agent")
    return current_agent
 
 
graph_builder = StateGraph(TutorState)

graph_builder.add_node(
    "classification_agent",
    classification_agent,  
    descriptions=( # descriptions 은 node에 연결된 edge는 없지만 하지만 이 노드가 두 에이전트로 전환시키는 tool이 있다는 걸 알고있음 이럴떄 사용 
        "teacher_agent",
        "feynman_agent"
        ),
    )
graph_builder.add_node("teacher_agent", teacher_agent )
graph_builder.add_node("feynman_agent", feynman_agent )

graph_builder.add_conditional_edges(
    START,
    router_check,
    [
        "teacher_agent",
        "feynman_agent",
        "classification_agent",
    ],
)
graph_builder.add_edge("classification_agent", END)

graph = graph_builder.compile()