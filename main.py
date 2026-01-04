import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import dotenv 
dotenv.load_dotenv() 
from openai import OpenAI
import asyncio # await과 같은 의미 
import streamlit as st 
import base64
from agents import (
    Agent,
    Runner, 
    SQLiteSession, 
    WebSearchTool, 
    FileSearchTool, 
    ImageGenerationTool,   # 인증문제로 잠시 주석 
    CodeInterpreterTool, 
    HostedMCPTool
)
from agents.mcp.server import MCPServerStdio

client = OpenAI()

VECTOR_STORE_ID = "vs_69524a97853c8191ab06435316ddc95b"
 
#세션 반복 생성 방지를 위해 "session_state" 가 없으면 세션 초기화  (처음 한번 생성)
if "session" not in st.session_state:
    st.session_state["session"] = SQLiteSession("chat-history", "chat-gpt-clone-memory.db")
session = st.session_state["session"]

# 챗팅 UI에 대화 기록을 보여주는 함수 
async def paint_history():
    messages = await session.get_items()

    for message in messages:
        if "role" in message:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    content = message["content"]
                    if isinstance(content,str):                            
                        st.write(message["content"])
                    elif isinstance(content,list):
                        for part in content:
                            if "image_url" in part:  # 이미지일떄 
                                st.image(part["image_url"])
                            
                else: # assistant 
                    if message["type"] == "message":
                        st.write(message["content"][0]["text"].replace("$", r"\$"))
        if "type" in message:
            message_type = message["type"]
            message_type = message["type"]
            if  message_type == "web_search_call":
                with st.chat_message("ai"):
                    st.write("🔎Searched the Web...") 
            elif  message_type == "file_search_call":
                with st.chat_message("ai"):
                    st.write("📁Searched your files...") 
            elif  message_type == "image_generation_call":
                image = base64.b64decode(message["result"])
                with st.chat_message("ai"):
                    st.image(image)
            elif message_type == "code_interpreter_call":
                with st.chat_message("ai"):
                    st.code(message["code"])
            elif message_type == "mcp_list_tools":
                with st.chat_message("ai"):
                    st.write(f"Listed {message['server_label']}'s tools")
            elif message_type == "mcp_call":
                with st.chat_message("ai"):
                    st.write(f"Called {message['server_label']}'s {message['name']} with args {message['arguments']}"
)


 
asyncio.run(paint_history())  # 이 함수로 인해 대화ui가 계속 이어짐. 없으면 기존 대화가 덮힘 (뭔말인지 모르겠으면 없애봐도됨)

# 상태 업데이트 
def update_status(status_container, event):
    
    status_messages = {
          "response.web_search_call.completed" :("✅ Web search completed.","complete"),
          "response.web_search_call.in_progres" : ("🔎 Starting web search...","running"),
          "response.web_search_call.searching" : ("🔎 Web search in progress...","running"),
          "response.file_search_call.completed" :("✅ File search completed.","complete"),
          "response.file_search_call.in_progres" : ("📁Starting file search...","running"),
          "response.file_search_call.searching" : ("📁 File search in progress...","running"),
          "response.image_generation_call.generating" : ("🖼️ Drawing image ...","running"),
          "response.image_generation_call.in_progress" : ("🖼️ Drawing image ...","running"),  
          'response.code_interpreter_call_code.done':("🤖 Ran Code.","complete") ,
          'response.code_interpreter_call.completed':("🤖 Ran Code.","complete") ,
          'response.code_interpreter_call.in_progress':("🤖 Running Code....","complete") ,
          'response.code_interpreter_call.interpreting':("🤖 Running Code....","complete") ,
          "response.mcp_call.failed": ("⚒️ Error calling MCP tool","complete",),
          "response.mcp_call.in_progress": ("⚒️ Calling MCP tool...","running",),
          "response.mcp_call.completed": ("⚒️ Listed MCP tools.","complete",),
          "response.mcp_call.failed": ("⚒️ Error listing MCP tools","complete",),
          "response.mcp_call.in_progress": ("⚒️ Listing MCP tools","complete",),
          "response.completed" : (" ","complete")
    }

    if event in status_messages:
        label, state = status_messages[event]
        status_container.update(label=label, state=state)
  

async def run_agent(message):

    # 1. 우선 서버가 실행되도록 만들어야한다.  
    yfinance_server = MCPServerStdio(
        params={
            "command": "uvx",
            "args": ["mcp-yahoo-finance"],
        },
        cache_tools_list = True, # tool 목록을 한번만 가져오고 캐싱 됨 . 
    )
    
    # 2. 서버를 with문으로 넣는다. 
    async with yfinance_server:  
        agent = Agent(
            mcp_servers=[yfinance_server],
            name = "ChatGPT Clone",
            # model="gpt-4o", 
            instructions="""
                You are a helpful assistant.

                You have access to the followign tools:
                - Web Search Tool: Use this when the user asks a questions that isn't in your training data. Use this tool when the users asks about current or future events, when you think you don't know the answer, try searching for it in the web first.
                - File Search Tool: Use this tool when the user asks a question about facts related to themselves. Or when they ask questions about specific files.
                - Code Interpreter Tool: Use this tool when you need to write and run code to answer the user's question.
        
            """, 
            tools =[
                WebSearchTool(),
                FileSearchTool(
                    vector_store_ids = [VECTOR_STORE_ID], # 각 유저마다 있으면 좋을듯하다함 
                    max_num_results=3, # 상위 파일 3개만 가져오는 
                ),
                # ImageGenerationTool(
                #     tool_config = {
                #         "type": "image_generation",      # 이미지 생성 타입 (맞음)
                #         "quality": "high",               # low가 더 저렴함. 이미지 품질 옵션 (보통 high/low 같은 단계) 
                #         "output_format": "jpeg",         
                #         "partial_images": 1,             # 중간 결과 이미지 개수 또는 단계 수를 의미하 
                #     }),
                CodeInterpreterTool(
                        tool_config={
                            "type": "code_interpreter", 
                            "container": {
                                "type": "auto",  #항상auto임 
                                # "file_ids" :  ["파일id"], # 이걸 하게 되면 모델에게 이전에 올렸던 파일에 대해 접근권한을 줄 수있다.(격리된 환경에서 파일을 제공할수있음)
                            },
                        }
                    ),
                HostedMCPTool(
                    tool_config={
                        "server_url": "https://mcp.context7.com/mcp",
                        "type": "mcp",
                        "server_label": "Context7",
                        "server_description": "Use this to get the docs from software projects.",
                        # 소프트웨어 프로젝트의 문서를 가져올 때 이것을 사용하시오 
                        "require_approval": "never", # always 로 하면 mcp가 tool을 사용할떄마다 나한테 확인받음 never로 하면 자유롭게 사용가능
                    }
                ), 
            ],
        )

        with st.chat_message("ai"):  
            status_container  = st.status("⌛", expanded=False) 
            code_placeholder = st.empty() 
            image_placeholder = st.empty()  # 이미지 컨테이너 비워주기 
            text_placeholder = st.empty() #비어있는 컨테이너 만들기         
            response = ""         
            code_response = ""
            
            # 유저가 새로운 메시지를 보낼떄만 비워주도록 위함 
            st.session_state["code_placeholder"] = code_placeholder
            st.session_state["image_placeholder"] = image_placeholder
            st.session_state["text_placeholder"] = text_placeholder        

            stream = Runner.run_streamed(agent, message,session = session)

            async for event in stream.stream_events():
                if event.type == "raw_response_event":

                    update_status(status_container, event.data.type)

                    if event.data.type == "response.output_text.delta":
                        response += event.data.delta
                        text_placeholder.write(response.replace("$", r"\$"))
                    
                    if event.data.type == "response.code_interpreter_call_code.delta":
                        # code의 delte를 받으면 agent가 코드를 써내려감 .  
                        code_response += event.data.delta
                        code_placeholder.code(code_response)
    
                    elif event.data.type == "response.image_generation_call.partial_image":
                        image = base64.b64decode(event.data.image_url)
                        image_placeholder.image(image) 


prompt = st.chat_input(
    "Write a message for your assistant",
    accept_file=True,
    file_type=["txt","jpg","jpeg","png","PNG"],
)

if prompt: 
 
    #새로운 프롬포트 입력받으면 비워주기 
    if "code_placeholder" in st.session_state:
        st.session_state["code_placeholder"].empty()
    if "image_placeholder" in st.session_state:
        st.session_state["image_placeholder"].empty()
    if "text_placeholder" in st.session_state:
        st.session_state["text_placeholder"].empty()

    for file in prompt.files:
        if file.type.startswith("text/"):
            with st.chat_message("ai"):
                with st.status("⏳ Uploading file...") as status:
                    uploaded_file = client.files.create(
                        file=(file.name, file.getvalue()),
                        purpose="user_data",
                    ) # 이 파일 다루는 방법은 streamlit한에서만 일수도있음 
                    status.update(label="⏳ Attaching file...")
                    client.vector_stores.files.create(
                        vector_store_id=VECTOR_STORE_ID,
                        file_id=uploaded_file.id,
                    )  # 벡터 스토어에 첨부 
                    status.update(label="✅ File uploaded", state="complete")
        elif file.type.startswith("image/"):
            with st.status("⏳ Uploading image...") as status:
                file_bytes = file.getvalue()
                base64_bytes = base64.b64encode(file_bytes).decode("utf-8")
                data_url = f"data:{file.type};base64,{base64_bytes}"
                asyncio.run(session.add_items([{
                    "role":"user",
                    "content":[{
                        "type": "input_image",
                        "image_url": data_url   
                    }]
                }]))
                status.update(label="✅ Image uploaded", state="complete")
            with st.chat_message("human"):
                st.image(data_url)

    if prompt.text:
        with st.chat_message("human"):
            st.write(prompt.text)
        asyncio.run(run_agent(prompt.text))

# 내 챗봇의 메모리를 볼 수 있는 디버깅 사이드바 만들기 , 또한 대화를 다시 시작하고 싶을 때를 위해 session을 지우는 버튼도 만든다. \
with st.sidebar:
    reset = st.button("Reset memory")
    if reset: # 버튼이 클릭됐을 때(True)
        asyncio.run(session.clear_session())  #session 지워짐 
    st.write(asyncio.run(session.get_items())) 