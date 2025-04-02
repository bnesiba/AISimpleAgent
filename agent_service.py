import json
import os
from typing import TypedDict, Annotated, Sequence
# from agent_tools import ask_the_human, get_weather, get_file_summaries, get_folder_summaries, get_top_5_folder_summaries, get_dir_structure, get_dir_structure_summary, get_project_summary
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt import ToolNode
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from langgraph.managed import IsLastStep, RemainingSteps
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate
from file_navigation_service import FileNavService
from langgraph.prebuilt import InjectedState
from langchain_core.tools import tool
from settings_loader import SettingsLoader


def load_data_from_file(file):
    with open(file, 'r') as f:
        fileJson = json.load(f)
        id = fileJson["id"]
        startPath = fileJson["startPath"]
        dirStructureString = fileJson["dirStructureString"]
        dirStructureSummary = fileJson["dirStructureSummary"]
        fileSummaryDict = fileJson["fileSummaryDict"]
        folderSummaryDict = fileJson["folderSummaryDict"]
        projectSummary = fileJson["projectSummary"]

        fileNav = FileNavService(startPath)
        fileNav.load_summaries(id, startPath, dirStructureString, dirStructureSummary, fileSummaryDict, folderSummaryDict, projectSummary)
        return fileNav

class TestAgentState(TypedDict):
        is_last_step: IsLastStep
        remaining_steps: RemainingSteps
        messages: Annotated[Sequence[BaseMessage], add_messages]

fileNav = load_data_from_file("C:\\Users\\brandon.nesiba\\source\\repos\\codebase results\\vuLoanReader-summarized.txt")

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

@tool
def get_file_content(agent_state: Annotated[TestAgentState, InjectedState], filePath: str) -> str:
    """Use this to get file content."""
    fileContent = open(filePath, "r").read()
    return fileContent

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






base_instructions = f"""# Persona
You are a helpful code assistant named Helpy. You have been given information and tools for a specific codebase.
Your job is to help the user (who is a software engineer at veterans united home loans) with tasks relating to that codebase. 
These tasks might include things like: understanding how a feature in implemented across the codebase, finding where a specific part of a feature is implemented, or suggesting how to implement a new feature.

# Project Information

*Project File Structure:*
{get_dir_structure()}

*Project Summary:*
file structure summary (written without knowledge of the content of the files):
{get_dir_structure_summary()}

summary of the project:
{get_project_summary()}

# Tool Information
Using the Project File Structure, you can get information about the files and folders in the project.
Use `get_folder_summaries` to get a summary of the content of any particular non-file directory in the project. This summary will also summarize any subdirectories in that directory.
Use `get_file_content` to get the actual text content of a specific file. Generally, it is best to use `get_folder_summaries` first to get a good idea what files to read before pulling the content of a specific file.
Use `get_file_summaries` to get a summary of a specific file. These summaries are so-so, but if you aren't sure if you need to read the file, this is a good way to try to verify.

You are a code assistant. You have tools that give info about the code for the current project. Use your tools to provide consise **SHORT** **As SHORT AS POSSIBLE** accurate answers to user prompts.

- Avoid LLM type words and phrases like "in conclusion", "delve", etc
- Be opinionated. Have and support the opinion that makes the most sense to you.
- Take a forward-thinking view.
- Adopt a skeptical, questioning approach.
- View the user's opinions and ideas with skepticism too.
- When giving feedback, be open an honest and not just a cheer leader.
- Do not just reflect the thoughts and opinions of the user, have your own.
- Take your time and make sure you fully understand how to resolve the prompt before responding. 
- Do as much of the work as you can for the user. Never tell the user to do something that you could do for them (unless asked). 
"""

# base_instructions = """# Persona
# You are a helpful assistant named Helpy. 
# Use your tools to provide consise **SHORT** **As SHORT AS POSSIBLE** accurate answers to user prompts."""

SettingsLoader()


prompt = ChatPromptTemplate.from_messages([
    ("system", base_instructions),
    ("placeholder", "{messages}")
])

memory = MemorySaver()#apparently this can only be used when not using `langgraph dev` command
# tools = ToolNode([get_weather, ask_the_human])
tools = ToolNode([get_file_summaries,get_folder_summaries, get_file_content])
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = tools
agent = create_react_agent(
    model=model,
    tools=tools,
    prompt=prompt   
)
# graph = agent.compile()


# display(Image(agent.get_graph().draw_mermaid_png()))

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


# inputs = {"messages": [("user", "what is the weather in sf")]}
# print_stream(agent.stream(inputs, stream_mode="values"))
