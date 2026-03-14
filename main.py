from typing import Literal, List
from langgraph import graph
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END 
from langgraph.checkpoint.memory import MemorySaver
from langchain.chat_models import init_chat_model

llm = init_chat_model("openai:gpt-4o") # ai모델 초기화 

checkpointer = MemorySaver()

class EmailState(TypedDict):
    email : str
    category : Literal["spam","normal","urgent"]
    priority_score : int
    response : str

class EmailClassificationOutput(BaseModel):
    category : Literal["spam","normal","urgent"] = Field(
        description="Category of the email"  
    ) # filed를 설명하면 그 description들이 ai model로 전달(ai모델이 더 명확하게 만들어줌줌)

class PriorityScoreOutput(BaseModel):
    priority_score : int = Field(
        description="Priority score from 1 to 10",
        ge = 1,
        le = 10,
    ) # pydantic을 사용하면 (field) 데이터의 생김새를 ai model에게 잘 설명가능하다

# 노드 추가 

# 이메일을 카테고리 별로 나누는 노드 
def categorize_email(state: EmailState):
    s_llm = llm.with_structured_output(EmailClassificationOutput)

    result = s_llm.invoke(
        f"""Classify this email into one of three categories:
        - urgent: time-sensitive, requires immediate attention
        - normal: regular business communication
        - spam: promotional, marketing, or unwanted content

        Email: {state['email']}"""
    )
    return {
        "category" : result.category
    }

# 우선순위 할당 노드 
def assing_priority(state: EmailState):
    s_llm = llm.with_structured_output(PriorityScoreOutput)

    result = s_llm.invoke(
        f"""Assign a priority score from 1-10 for this {state['category']} email.
        Consider:
        - Category: {state['category']}
        - Email content: {state['email']}

        Guidelines:
        - Urgent emails: usually 8-10
        - Normal emails: usually 4-7
        - Spam emails: usually 1-3"""
    )

    return {"priority_score": result.priority_score}

# 응답 
def draft_response(state: EmailState) -> EmailState:
    result = llm.invoke(
        f"""Draft a brief, professional response for this {state['category']} email.

        Original email: {state['email']}
        Category: {state['category']}
        Priority: {state['priority_score']}/10

        Guidelines:
        - Urgent: Acknowledge urgency, promise immediate attention
        - Normal: Professional acknowledgment, standard timeline
        - Spam: Brief notice that message was filtered

        Keep response under 2 sentences."""
    )
    return {
        "response": result.content,
    }


graph_builder = StateGraph(EmailState)

graph_builder.add_node("categorize_email", categorize_email)
graph_builder.add_node("assing_priority", assing_priority)
graph_builder.add_node("draft_response", draft_response)

graph_builder.add_edge(START, "categorize_email")
graph_builder.add_edge("categorize_email", "assing_priority")
graph_builder.add_edge("assing_priority", "draft_response")
graph_builder.add_edge("draft_response", END)

graph = graph_builder.compile(checkpointer= checkpointer)

# # 테스트 
# #result = graph.invoke({"email" : "i need to talk to you urgently"})
# result = graph.invoke({"email" : "i have an offer for you"})

# print(result)