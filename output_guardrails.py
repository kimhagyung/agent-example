from agents import Agent, output_guardrail, Runner, RunContextWrapper, GuardrailFunctionOutput  # 가드레일은 Runner로 돌린다. 
from models import TechnicalOutputGuardRailOutput , UserAccountContext

technical_output_guardrail_agent = Agent( # 에이전트의 응답을 분석해서 이 항목들중에서 포함이 되었는지 확인하라고 하는 것(만약 포함되어 잇다면문제가 있는것)
    name="Technical Support Guardrail",
    instructions="""
    Analyze the technical support response to check if it inappropriately contains:
    
    - Billing information (payments, refunds, charges, subscriptions)
    - Order information (shipping, tracking, delivery, returns)
    - Account management info (passwords, email changes, account settings)
    
    Technical agents should ONLY provide technical troubleshooting, diagnostics, and product support.
    Return true for any field that contains inappropriate content for a technical support response.
    """,
    output_type=TechnicalOutputGuardRailOutput,
)

@output_guardrail
async def technical_output_guardrail(
    wrapper : RunContextWrapper[UserAccountContext],
    agent : Agent, 
    output : str,
): 
    result = await Runner.run(
        technical_output_guardrail_agent,
        output, 
        context = wrapper.context
    ) 

    validation = result.final_output
    
    # 응답주제에서 벗어나 있는지 여부를 걸러내는 검증 or 입력안에 결제관련 정보가 포함돼 있는지 확인 or 계정과 관련된 데이터가 들어있는지확인
    triggered = ( 
        validation.contains_off_topic 
        or validation.contains_billing_data
        or validation.contains_accouts_data
    )

    return GuardrailFunctionOutput(
        output_info = validation,
        tripwire_triggered=triggered # trip_wire 가 발동됐는지 확인 
    )
 