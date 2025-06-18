
#!/usr/bin/env python3.9
import logging
import os
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
from langchain_core.messages import HumanMessage
import asyncio
import agent_service
from models.agent_models import AgentMessage
from langgraph.types import Command
from signalr_service import SignalREvents, SignalRService
# Log filtering config: Filter out access logs for /health and /openapi.json

class ReadinessFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/ready") == -1

class LivenessFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/self") == -1

class MetricsFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/metrics") == -1

class OpenAPIFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/openapi.json") == -1

logging.getLogger("uvicorn.access").addFilter(ReadinessFilter())
logging.getLogger("uvicorn.access").addFilter(LivenessFilter())
logging.getLogger("uvicorn.access").addFilter(MetricsFilter())
logging.getLogger("uvicorn.access").addFilter(OpenAPIFilter())


# FastAPI models

def getVersionNumber() -> str:
    """Get version number from a file in the repo. To be populated by the CI/CD
    pipeline.
    """
    with open('./version') as f:
        version = f.read().rstrip()

    return version

def getRootPath() -> str:
    """Get the root path from the environment if it exists. Otherwise leave it
    blank.
    """

    baseHref = os.environ.get('BASE_HREF')

    return baseHref if baseHref is not None else ""
    
    

# Create the app here
app = fastapi.FastAPI(
        title='AgentApi', # API docs title
        description='Api interface for agent chatbot', # API description
        version=getVersionNumber(),
        root_path=getRootPath(),
        docs_url='/swagger',
        )
origins = ["*"];
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Task to clean up idle sessions
async def cleanup_sessions():
    while True:
        print("(not really) Cleaning up idle sessions...")
        await asyncio.sleep(1800)

@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(cleanup_sessions())

# Use decorators to define the HTTP method
@app.get(
        '/self',
        summary="Liveness probe.",
        tags=['Health']
        )
def api_sel():
    return "OK"

@app.get(
        '/ready',
        summary="Readiness probe",
        tags=['Health']
        )
def api_ready():
    return "OK"

##***************** FastAPI endpoint Setup *****************##
#defining endpoints for REST controllers/routes in the API

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/Chat/{sessionId}")
def run_chat(sessionId, message: str = Body()):
    initialState = {
        "messages": [HumanMessage(content=message)],
    }
    config = {"configurable": {"thread_id": sessionId}}
    result = agent_service.agent.invoke(initialState, config)
    return result


@app.post("/StreamChat/{sessionId}")
async def run_chat(sessionId, message: str = Body()):

    config = {"configurable": {"thread_id": sessionId}, "recursion_limit":50}
    result = ""
    initialState = {
        "messages": [HumanMessage(content=message)],
        "references": [],
    }

    agentInterrupts = agent_service.agent.get_state(config=config).interrupts
    if agentInterrupts and len(agentInterrupts) > 0:
        print("Agent has interrupt, handling")
        initialState = Command(resume=message)

    streamingConnected = SignalRService.send(sessionId, "START-OF-STREAM", msgType=SignalREvents.Message_Start.value)

    for msg, metadata in agent_service.agent.stream(initialState, config, stream_mode="messages"):
        if(msg.content != "" and metadata["langgraph_node"] == "agent"):
            if(streamingConnected): #to save time, only stream if the START-OF-STREAM was sent successfully, otherwise assume signalr is down. 
                SignalRService.send(sessionId, msg.content)

            result += msg.content

    SignalRService.send(sessionId, "END-OF-STREAM", msgType=SignalREvents.MESSAGE_COMPLETE.value) #might not be needed. could be used for references?

    agentInterrupts = agent_service.agent.get_state(config=config).interrupts
    responseMetadata = []
    for interrupt in agentInterrupts:
        print(interrupt.value)
        responseMetadata.append(interrupt.value)

    agentResponse = AgentMessage(message=result, sessionId=sessionId, chatReferences=agent_service.agent.get_state(config=config)[0].get("references"), metadata=responseMetadata)
    return agentResponse.to_dict()


@app.get("/chat/{sessionId}")
async def run_chat(sessionId):
    config = {"configurable": {"thread_id": sessionId}}
    stateObj = agent_service.agent.get_state(config=config)[0].get("messages")
    
    return stateObj

# @app.post("/codeReader/Chat/{sessionId}")
# def run_chat(sessionId, message: str = Body()):
#     return CodeReaderChatService.RunCodeSearchBot(message, sessionId);


##***************** End FastAPI Setup *****************##
