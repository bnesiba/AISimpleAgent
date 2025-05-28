from typing import Annotated
from langchain_core.tools import tool
from tools.FileNavigationService import FileNavService
from models.agent_models import AgentMessageReference
from langchain_core.messages import ToolMessage  # Import ToolMessage
from langgraph.types import Command
from langgraph.types import interrupt
from langchain_core.tools.base import InjectedToolCallId


@tool
def get_file_text(filePath: str, tool_call_id: Annotated[str, InjectedToolCallId]) -> str:
    """Get the text of a specified file in your codebase. Use get_file_structure to get file paths."""
    print("getting file text...")
    fileNav = FileNavService()
    file_text = fileNav.get_file_text(filePath)
    full_path = fileNav.get_full_path(filePath)
    refToAdd = AgentMessageReference(f">Read: {filePath} ",f"{full_path}").to_dict()
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
    """Get the structure of the files and directories in your codebase."""
    print("getting file structure...")
    fileNav = FileNavService()
    dir_structure = fileNav.generate_dir_structure()
    # human_result = InterruptWithConfirmation(f"Interrupting directory structure...")
    # print(f"Human result: {human_result}")
    return dir_structure

@tool
def update_file_text(filePath: str, newText: str, tool_call_id: Annotated[str, InjectedToolCallId]) -> str:
    """Update the text of a specified file in your codebase. Use get_file_text to get the current text before providing your updated text.
    The provided text will overwrite the existing file content, make sure to include the full text of the file."""
    print(f"updating file text... {filePath}")

    human_response = InterruptWithConfirmation(f"These are the changes I am about to make to the file. Would you like me to make them?\n\n {newText}")
    print(f"Human response: {human_response}")
    if human_response.lower() != "yes":
        print("Update cancelled by user.")
        return "Update cancelled by user."
    
    fileNav = FileNavService()
    fileNav.update_file_text(filePath, newText)
    print(f"File {filePath} updated successfully.")
    full_path = fileNav.get_full_path(filePath)

    refToAdd = AgentMessageReference(f">Updated: {filePath} ",f"{full_path}").to_dict()
    return Command(
        update={
            "references": [refToAdd],
            "messages":[
                ToolMessage(newText,tool_call_id=tool_call_id)
            ]
        }
    )

# @tool
# def do_the_confirmation_thing() -> str:
#     """A tool that does the confirmation thing."""
#     human_result =  InterruptWithConfirmation("I'm about to do the thing. You cool with that?")
#     print(f"Human result: {human_result}")
#     if( human_result.lower() == "yes"):
#         return "User approved. Thing done."
#     else:
#         return "User disapproved. Thing not done."
    

#TODO: organize these somewhere else? Set up enums for types
def InterruptWithConfirmation(message: str) -> str:
    """Interrupt the agent with a confirmation message."""
    return interrupt({"metadataType":"interrupt-confirmation", "payload": message})

# @staticmethod
# def InterruptWithError(message: str) -> str:
#     """Interrupt the agent with an error message."""
#     return interrupt({"metadataType":"error", "payload": message})