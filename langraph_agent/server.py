# fast api 사용 
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Request
from graph import graph 

app = FastAPI()

def run_graph(message:str):
    result = graph.invoke({"messages" : [{"role": "user", "content" : message}]})
    return result["messages"][-1].content

# agent-card를 먼저 노출할것임. 
@app.get("/.well-known/agent-card.json")
def get_agent_card(): 
    return{
        "capabilities": {

        },
        "defaultInputModes": [
            "text/plain"
        ],
        "defaultOutputModes": [
            "text/plain"
        ],
        "description": "An agent that can help  students with philosophy homework",
        "name": "PhilosophyHelperAgent",
        "preferredTransport": "JSONRPC",
        "protocolVersion": "0.3.0",
        "skills": [
            {
            "description": "An agent that can help  students with philosophy homework",
            "id": "PhilosophyHelperAgent",
            "name": "model",
            "tags": [
                "llm"
            ]
            },
        ],
        "supportsAuthenticatedExtendedCard": False,
        "url": "http://localhost:8002/",
        "version": "0.0.1"
        }

@app.post("/")
async def handle_messages(req: Request):
    body = await req.json()
    messages = body.get("params").get("message").get("parts")
    messages.reverse()
    message_text = ""
    for message in messages:
        text = message.get("text")
        message_text += f"{text}\n"
    response = run_graph(message_text)
    return {
        "message" : response
    }

