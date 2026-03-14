import dotenv 
dotenv.load_dotenv()
import pytest
from pydantic import BaseModel, Field
from main import graph 
from langchain.chat_models import init_chat_model

llm = init_chat_model("openai:gpt-4o") # ai모델 초기화 

class SimilaritySCoreOutput(BaseModel):
    similarity_score : int = Field(
        description="How similar is the response to the examples?", # 우리가 그래프에서 받은 response가 그 examples와 얼마나 비슷한지 
        gt=0,
        lt=100
    )

  # 예시들      
RESPONSE_EXAMPLES = {
    "urgent": [
        "Thank you for your urgent message. We are addressing this immediately and will respond as soon as possible.",
        "We've received your urgent request and are prioritizing it. Our team is on it right away.",
        "This urgent matter has our immediate attention. We'll respond promptly.",
    ],
    "normal": [
        "Thank you for your email. We'll review it and get back to you within 24-48 hours.",
        "We've received your message and will respond soon. Thank you for reaching out.",
        "Thank you for contacting us. We'll process your request and respond shortly.",
        "Thank you for the update. I will review the information and follow up as needed.",
        "Thank you for the update on the project status. I will review and follow up by the end of the week.",
        "Thanks for sharing this update. We'll review and respond accordingly.",
    ],
    "spam": [
        "This message has been flagged as spam and filtered.",
        "This email has been identified as promotional content.",
        "This message has been marked as spam.",
    ],
}

def judge_response(response : str, category : str):
    s_llm = llm.with_structured_output(SimilaritySCoreOutput) 

    examples = RESPONSE_EXAMPLES[category]
    # examples를 사용하는 뭔가 작성 (response가 얼마나 examples와 비슷한지 알려주는 그런것)
    # 아래 Score 은 이 response가 examples와 얼마나 비슷한지를 나타냄 
    result = s_llm.invoke(
        f"""
        Score how similar this response is to the examples.

        Category: {category}

        Examples:
        {"\n".join(examples)}

        Response to evaluate:
        {response}

        Scoring criteria:
        - 90-100: Very similar in tone, content, and intent
        - 70-89: Similar with minor differences
        - 50-69: Moderately similar, captures main idea
        - 30-49: Some similarity but missing key elements
        - 0-29: Very different or inappropriate

    """
    )

    return result.similarity_score


# decorator 가 아래 순서로 함수를 호출하고 arg를 전달 
@pytest.mark.parametrize(
    #  우리가 할 일이 뭔가를 적는다. (기본적으로 여러 argument(인자)들의 순서를 적는다. )
    "email, expected_category, min_score, max_score",
    [
        ("this is urgent!", "urgent", 8, 10), 
        ("i wanna talk to you", "normal", 4, 7), 
        ("i have an offer for you", "spam", 1 ,3), 
    ]
)
def test_full_graph(email, expected_category, min_score, max_score):
    result = graph.invoke({"email"  : email}, config={"configurable" : {"thread_id" : "1"}})
    # assert : 조건을 쓸 수 있게 해주는 파이썬 키워드, 만약조건이 참이 아니면 assert가 일종의 에러를 만든다. (이게다임)
    # 아래는 우리가 기대하는 것들이 맞는지 assert(확인) 하고있는 것 
    assert result["category"] == expected_category
    assert min_score <= result["priority_score"]  <= max_score

# 노드가 필요로 했던 state와 함께 node를 invoke함으로써 노드를 각각 따로따로 테스트한다.  
def test_individual_nodes():
    # categorize_email

    result = graph.nodes["categorize_email"].invoke({"email": "check out this offer"})

    assert result["category"] == "spam"

    # assing_priority

    result = graph.nodes["assing_priority"].invoke(
        {"category": "spam", "email": "buy this pot."}
    )

    assert 1 <= result["priority_score"] <= 3
    
    # draft_response    
    result = graph.nodes["draft_response"].invoke( # 특정 노드만 invoke
        {
            "category" : "spam",
            "email" : "Get rich quick!! I have a pyramid scheme for you!",
            "priority_score" : 1,
        } # draft_response 에 필요한 모든 state가 있는지 확인 
    )

    simiarity_score = judge_response(result["response"], "spam")
    assert  simiarity_score >= 70 

# 부분 노드 실행 
def test_partial_execution():
    graph.update_state(
        config = {
            "configurable" :{
                "thread_id" : "1",
            }, 
        },
        values={ # 업데이트 하고 싶은 value
            "email" : "please check out this offer.",
            "category" : "spam"
        },
        as_node= "categorize_email" ,# 마치 노드처럼 , categorize_email 노드인척 
    )

    result = graph.invoke(
        None, 
        config = {
            "configurable" :{
                "thread_id" : "1",
            }, 
        },
        interrupt_after=  "draft_response"  # 원하는 지점에서 중담(intterup_before도 있음 )
    )

    assert 1 <= result["priority_score"]  <= 3