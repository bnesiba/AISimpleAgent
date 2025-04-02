from langchain_core.tools import tool
from typing import Annotated, Literal
from langgraph.prebuilt import InjectedState
from langgraph.types import interrupt, Command

from agent_service import TestAgentState
from file_navigation_service import FileNavService

@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")


@tool
def ask_the_human(agent_state: Annotated[dict, InjectedState], question: str) -> str:
    """Use this to ask the human a question."""
    print(agent_state)
    humanAnswer = interrupt(
        {
            "question": question
            # Surface the output that should be
            # reviewed and approved by the human.
        }
    )
    return humanAnswer


@tool
def get_file_summaries(agent_state: Annotated[TestAgentState, InjectedState], dirPath: str) -> str:
    """Use this to get file summaries."""
    fileSummaries = fileNav.get_file_summaries(dirPath)
    return "\n".join(fileSummaries)

@tool
def get_folder_summaries(agent_state: Annotated[TestAgentState, InjectedState], dirPath: str) -> str:
    """Use this to get folder summaries."""
    folderSummaries = fileNav.get_folder_summaries(dirPath)
    return "\n".join(folderSummaries)

def get_top_5_folder_summaries() -> str:
    """Use this to get the top 5 folder summaries."""
    folderSummaries = fileNav.get_top_5_folder_summaries()
    return "\n".join(folderSummaries)

def get_dir_structure() -> str:
    """Use this to get the directory structure."""
    return fileNav.dirStructureString

def get_dir_structure_summary() -> str:
    """Use this to get the directory structure summary."""
    return fileNav.dirStructureSummary

def get_project_summary() -> str:
    """Use this to get the project summary."""
    return fileNav.projectSummary