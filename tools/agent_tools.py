from typing import Annotated
from langchain_core.tools import tool
from FileNavigationService import FileNavService
from models.agent_models import AgentMessageReference
from langchain_core.messages import ToolMessage  # Import ToolMessage
from langgraph.types import Command
from langchain_core.tools.base import InjectedToolCallId


@tool
def get_file_text(filePath: str, tool_call_id: Annotated[str, InjectedToolCallId]) -> str:
    """Get the text of a specified file. Use get_file_structure to get file paths."""
    print("getting file text...")
    fileNav = FileNavService()
    file_text = fileNav.get_file_text(filePath)
    full_path = fileNav.get_full_path(filePath)
    refToAdd = AgentMessageReference(f"> Read: {filePath} ",f"{full_path}").to_dict()
    return Command(
        update={
            "references": [refToAdd],
            "messages":[
                ToolMessage(file_text,tool_call_id=tool_call_id)
            ]
        }
    )


@tool
def get_file_structure() -> str:
    """Get the structure of the files and directories in the project."""
    print("getting file structure...")
    fileNav = FileNavService()
    dir_structure = fileNav.generate_dir_structure()
    return dir_structure