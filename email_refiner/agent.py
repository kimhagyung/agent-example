from google.adk.agents import Agent, LoopAgent
from google.adk.models.lite_llm import LiteLlm
from .prompt import (
    EMAIL_OPTIMIZER_DESCRIPTION,
    TONE_STYLIST_DESCRIPTION,
    CLARITY_EDITOR_DESCRIPTION,
    LITERARY_CRITIC_DESCRIPTION,
    EMAIL_SYNTHESIZER_DESCRIPTION,
    PERSUASION_STRATEGIST_DESCRIPTION,
    TONE_STYLIST_INSTRUCTION,
    CLARITY_EDITOR_INSTRUCTION,
    LITERARY_CRITIC_INSTRUCTION,
    EMAIL_SYNTHESIZER_INSTRUCTION,
    PERSUASION_STRATEGIST_INSTRUCTION,
)
from google.adk.tools.tool_context import ToolContext

MODEL = LiteLlm(model="openai/gpt-4o")

clarity_agent = Agent(
    name="ClarityEditorAgent",
    description=CLARITY_EDITOR_DESCRIPTION,
    instruction=CLARITY_EDITOR_INSTRUCTION,
    output_key = "clarity_output",  # state변수로 관리  
    model = MODEL
)

tone_stylist_agent = Agent(
    name="ToneStylistAgent",
    description=TONE_STYLIST_DESCRIPTION,
    instruction=TONE_STYLIST_INSTRUCTION,
    output_key = "tone_output",
    model = MODEL
)

persuation_agent = Agent(
    name="PersuationAgent",
    description=PERSUASION_STRATEGIST_DESCRIPTION,
    instruction=PERSUASION_STRATEGIST_INSTRUCTION,
    output_key="persuasion_output",
    model = MODEL
)

email_synthesizer_agent = Agent(
    name="EmailSynthesizerAgent",
    description=EMAIL_SYNTHESIZER_DESCRIPTION,
    instruction=EMAIL_SYNTHESIZER_INSTRUCTION,
    output_key = "synthesized_output",
    model = MODEL
) 

def escalate_email_complete(tool_context: ToolContext):
    """ Use this tool only when the email is good to go."""
    tool_context.actions.escalate = True  # 루프 종료됨 (계층구조라면 하위 에이전트에서 루프가 종료됐을 때 바로 상위 에이전트로 제어권이 넘겨짐)
    return "Email optimization complete" #이메일 최적화 완료

literary_critic_agent = Agent(
    name="LiteraryCriticAgent",
    description=LITERARY_CRITIC_DESCRIPTION,
    instruction=LITERARY_CRITIC_INSTRUCTION,
    tools=[
        escalate_email_complete
    ],
    model = MODEL
)

email_refiner_agent = LoopAgent(
    name = "Email_Refiner_Agent",
    max_iterations=50, # 50번 반복후 종료 (조건1)
    description = EMAIL_OPTIMIZER_DESCRIPTION,
    sub_agents=[ # 내가 원하는 순서로 ㅇ넣어야함 (sequential agent처럼 순서가 중요함)
        clarity_agent,
        tone_stylist_agent,
        persuation_agent,
        email_synthesizer_agent,
        literary_critic_agent, 
    ]
)

# 사용자가 agent에게 메시지를 보내느 순간 agent는 즉시 모든 sub agent를 동작시킴 (추론, 대화 다 없고 agnet와 유저가 주고받는것도 없이 그냥 하위 에이전트를 실행시킴)
# 만약 agent가 바로 시작하길 원하지 않는다면 
# loopagent를 만들지 말고, loopagnet를 tool로 가진 agent나 sub agent둘 중 하나를 만들어야함 
root_agent = email_refiner_agent  