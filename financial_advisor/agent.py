from google.genai import types # google ai api와 상호작용하는 ptyhon 클라이언트 라이브러리임. 
from google.adk.tools import ToolContext
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.models.lite_llm import LiteLlm
from .sub_agents.data_analyst import data_analyst
from .sub_agents.financial_analyst import financial_analyst
from .sub_agents.news_analyst import news_analyst
from .prompt import PROMPT

MODEL = LiteLlm("openai/gpt-4o")

# financial_advisor가 사용자가 레포트를 저장하고 싶을 때 호출할 tool(사용자가 이 조언으로 리포트를 만들고 싶다 했을 때 호출하게 될 툴임. )
# finacial_advisor가 artifact api를 사용해서 그 파일을 저장하고 나면 파일이 artifacts box에 나타남
async def save_advice_report(tool_context: ToolContext, summary: str, ticker: str):
    state = tool_context.state
    data_analyst_result = state.get("data_analyst_result")
    financial_analyst_result = state.get("financial_analyst_result")
    news_analyst_analyst_result = state.get("news_analyst_analyst_result")
    report = f"""
        # Excetuve Summary and Advice:
        {summary}

        ## Data Analyst Report:
        {data_analyst_result}

        ## Financial Analyst Report:
        {financial_analyst_result}
        
        ## News Analyst Report:
        {news_analyst_analyst_result}
    """
    state["report"] = report

    filename = f"{ticker}_investment_advice.md"

    # 파일 만드는 거임! (google.genai 사용 )
    artifact = types.Part(  # types는 그냥 pydantic model 뭉치임 
        inline_data=types.Blob(
            mime_type="text/markdown",
            data=report.encode("utf-8"),
        )
    )

    await tool_context.save_artifact(filename, artifact)

    return {
        "success": True,
    }


financial_advisor = Agent(
    name="financial_analyst",
    instruction=PROMPT,
    model=MODEL,
    tools=[
        AgentTool(agent=financial_analyst),
        AgentTool(agent=news_analyst),
        AgentTool(agent=data_analyst),
        save_advice_report,
    ],
)

root_agent = financial_advisor