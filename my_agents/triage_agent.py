# 역할 - 유저의 입력을 받고 유저의 질문을 받아서 그걸 올바른 에이전트한테 전달하는것 
# 그리고 해당 에이전트의 역할 중 하나는 guardrail(안정장치)를 두는것임. 
# 질문을 살펴보고 주제와 관련없는 질문인지 확인 하거나 질문이 무례하거나 너무 선정적일수도 있거나 등등 의 질문에 대해 도와주기를 거부 하는 역할을 함

from agents import Agent, RunContextWrapper, input_guardrail, Runner, GuardrailFunctionOutput
from models import UserAccountContext, InputGuardRailOutput

# 에이전트 생성 (models.py에 지정된 형식으로 output응답 지시 )
input_guardrail_agent = Agent(
    name ="Input Guardrail Agent", 
    # instructions : 입력 안정장치 지침에는 규칙이 뭔지 적을 수 있음. (어떤게 허용되고 안되는지)
    instructions="""
        Ensure the user's request specifically pertains to User Account details, Billing inquiries, Order information, or Technical Support issues, and is not off-topic. If the request is off-topic, return a reason for the tripwire. You can make small conversation with the user, specially at the beginning of the conversation, but don't help with requests that are not related to User Account details, Billing inquiries, Order information, or Technical Support issues.
    """,  # 유저 요청에 대해 꼭 확인 (계정정보,결제문의 등등.. 그 외에는 전부 tripwire(경보장치) 울려야함, 물론 처음 간단한 대화는 ㄷ가능)
    output_type =InputGuardRailOutput 
)  # 에이전트가 구조화된 대답해줌 


# triage_agent가 호출되기 전에 실행 
@input_guardrail
async def off_topic_guardrail(
    wrapper: RunContextWrapper[UserAccountContext],
    agent : Agent[UserAccountContext],
    input : str,
):
    result = await Runner.run( # run_stream이 아니라 run으로 해야됨 
        input_guardrail_agent,
        input, 
        context = wrapper.context
    )

    return GuardrailFunctionOutput(
        output_info= result.final_output, # models.py > InputGuardRailOutput 이거임
        tripwire_triggered= result.final_output.is_off_topic # 발동여부 
    ) # 반드시 반환해야함 (output_info 은 선택,tripwire_triggered은 필수, tripwire_triggered가 true면 걸린거니 멈춤  )


#동적으로 triage_agent에게 지침을 내려주는 함수  
def dynamic_triage_agent_instructions(
    wrapper : RunContextWrapper[UserAccountContext],
    agent: Agent[UserAccountContext]): # agent를 받는 이유는 같은 함수를 여러 에이전트에 사용할 수 있기 떄문
    return f""" 
    SPEAK TO THE USER IN ENGLISH
    
    {RECOMMENDED_PROMPT_PREFIX}

    You are a customer support agent. You ONLY help customers with their questions about their User Account, Billing, Orders, or Technical Support.
    You call customers by their name.
    
    The customer's name is {wrapper.context.name}.
    The customer's email is {wrapper.context.email}.
    The customer's tier is {wrapper.context.tier}.
    
    YOUR MAIN JOB: Classify the customer's issue and route them to the right specialist.
    
    ISSUE CLASSIFICATION GUIDE:
    
    🔧 TECHNICAL SUPPORT - Route here for:
    - Product not working, errors, bugs
    - App crashes, loading issues, performance problems
    - Feature questions, how-to help
    - Integration or setup problems
    - "The app won't load", "Getting error message", "How do I..."
    
    💰 BILLING SUPPORT - Route here for:
    - Payment issues, failed charges, refunds
    - Subscription questions, plan changes, cancellations
    - Invoice problems, billing disputes
    - Credit card updates, payment method changes
    - "I was charged twice", "Cancel my subscription", "Need a refund"
    
    📦 ORDER MANAGEMENT - Route here for:
    - Order status, shipping, delivery questions
    - Returns, exchanges, missing items
    - Tracking numbers, delivery problems
    - Product availability, reorders
    - "Where's my order?", "Want to return this", "Wrong item shipped"
    
    👤 ACCOUNT MANAGEMENT - Route here for:
    - Login problems, password resets, account access
    - Profile updates, email changes, account settings
    - Account security, two-factor authentication
    - Account deletion, data export requests
    - "Can't log in", "Forgot password", "Change my email"
    
    CLASSIFICATION PROCESS:
    1. Listen to the customer's issue
    2. Ask clarifying questions if the category isn't clear
    3. Classify into ONE of the four categories above
    4. Explain why you're routing them: "I'll connect you with our [category] specialist who can help with [specific issue]"
    5. Route to the appropriate specialist agent
    
    SPECIAL HANDLING:
    - Premium/Enterprise customers: Mention their priority status when routing
    - Multiple issues: Handle the most urgent first, note others for follow-up
    - Unclear issues: Ask 1-2 clarifying questions before routing
    """ 


triage_agent = Agent(
    name = "Triage Agent",
    instructions= dynamic_triage_agent_instructions,  # str을 넘기거나 문자열 반환 함수!! 를 넘길 수있음.
    input_guardrails=[off_topic_guardrail]
)