from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import START, END, StateGraph, MessagesState
from agent.classification_agent import classification_agent
from agent.teacher_agent import teacher_agent
from agent.feynman_agent import feynman_agent

class TutorState(MessagesState):
    pass 
 
graph_builder = StateGraph(TutorState)

graph_builder.add_node("classification_agent", classification_agent )
graph_builder.add_node("teacher_agent", teacher_agent )
graph_builder.add_node("feynman_agent", feynman_agent )

graph_builder.add_edge(START, "classification_agent")
 
graph = graph_builder.compile()