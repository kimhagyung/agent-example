
import pytest
from main import graph 

# decorator 가 아래 순서로 함수를 호출하고 arg를 전달 
@pytest.mark.parametrize(
    #  우리가 할 일이 뭔가를 적는다. (기본적으로 여러 argument(인자)들의 순서를 적는다. )
    "email, expected_category, expected_score",
    [
        ("this is urgent!", "urgent", 10), 
        ("i wanna talk to you", "normal", 5), 
        ("i have an offer for you", "spam", 1), 
    ]
)
def test_full_graph(email, expected_category, expected_score):
    result = graph.invoke({"email"  : email})

    # assert : 조건을 쓸 수 있게 해주는 파이썬 키워드, 만약조건이 참이 아니면 assert가 일종의 에러를 만든다. (이게다임)
    # 아래는 우리가 기대하는 것들이 맞는지 assert(확인) 하고있는 것 
    assert result["category"] == expected_category
    assert result["priority_score"] ==  expected_score 