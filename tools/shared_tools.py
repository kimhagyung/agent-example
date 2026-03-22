import re
import os
from langgraph.types import Command
from langchain_core.tools import tool
from firecrawl import FirecrawlApp, ScrapeOptions

# 여기서 agent의 이름을 받고 그  agent로 전환 
# 해당 tool이 서브 그래프에서 호출되면 부모  그래프에 있는 노드로 전환시켜 달라고 해야함. 
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

@tool
def web_search_tool(query: str):
    """
    Web Search Tool.
    Args:
        query: str
            The query to search the web for.
    Returns
        A list of search results with the website content in Markdown format.
    """
    app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

    response = app.search(
        query=query,
        limit=5,
        scrape_options=ScrapeOptions(
            formats=["markdown"],
        ),
    )

    if not response.success:
        return "Error using tool."

    cleaned_chunks = []

    for result in response.data:

        title = result["title"]
        url = result["url"]
        markdown = result["markdown"]

        cleaned = re.sub(r"\\+|\n+", "", markdown).strip()
        cleaned = re.sub(r"\[[^\]]+\]\([^\)]+\)|https?://[^\s]+", "", cleaned)

        cleaned_result = {
            "title": title,
            "url": url,
            "markdown": cleaned,
        }

        cleaned_chunks.append(cleaned_result)

    return cleaned_chunks