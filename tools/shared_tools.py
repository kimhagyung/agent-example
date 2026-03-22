from langchain_core.tools import tool
from langgraph.types import Command

# 여기서 agent의 이름을 받고 그  agent로 전환 
# 해당 tool이 서브 그래프에서 호출되면 부모 그래프에 있는 노드로 전환시켜 달라고 해야함. 
@tool
def transfer_to_agent(agent_name : str):
    """
    Transfer to the given agent 

    Args :   
        agent_name : Name of the agent to transfer to, one of: quiz_agent, teacher_agnet or 
        'feynman_agent'  
    """ # 이 tool은 이 중 하나의 에이전트로 전환된다.  

    return f"Transfer to {agent_name} completed." # 분류에이전트ㅡ 전환 발생 콘솔 기록 (분류 함수 테스트)

    # return Command(
    #     goto=agent_name, 
    #     graph=Command.PARENT
    # )

