import dotenv 

dotenv.load_dotenv()

import pytest
from main import graph 

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
    # result = graph.nodes["draft_response"].invoke( # 특정 노드만 invoke
    #     {"category" : "spam"}
    # )

    # assert "Go away!" in result["response"]  

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