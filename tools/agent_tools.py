from typing import Annotated
from langchain_core.tools import tool
from models.agent_models import AgentMessageReference
from langchain_core.messages import ToolMessage  # Import ToolMessage
from langgraph.types import Command
from langchain_core.tools.base import InjectedToolCallId


@tool
def do_the_thing(tool_call_id: Annotated[str, InjectedToolCallId]) -> str:
    """Do the thing the user is asking for"""
    print("doing the thing...")
    refToAdd = AgentMessageReference("> Doing the thing reference","https://example.com/doing_the_thing").to_dict()
    return Command(
        update={
            "references": [refToAdd],
            "messages":[
                ToolMessage("Thing successfully done! Doing the thing creates a reference for the user",tool_call_id=tool_call_id)
            ]
        }
    )


@tool
def do_the_other_thing() -> str:
    """Do the thing the user is asking for"""
    print("doing the other thing...")
    return "Other thing has been done! Doing the other thing does not create a reference for the user."