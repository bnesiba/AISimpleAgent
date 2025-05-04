import json
from operator import add
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
from langgraph.prebuilt import InjectedState
from langchain_core.tools import tool
from models.agent_models import AgentMessageReference, merge_ref_lists
from settings_loader import SettingsLoader
from tools.agent_tools import do_the_other_thing, do_the_thing



class InternalAgentState(TypedDict):
        is_last_step: IsLastStep
        remaining_steps: RemainingSteps
        messages: Annotated[Sequence[BaseMessage], add_messages]
        references: Annotated[list[AgentMessageReference], merge_ref_lists]




base_instructions = f"""# Persona
You are a helpful assistant named Helpy. <Your specific purpose goes here>
Your job is to help the user (who is a person) with tasks or information. 
These tasks might include things like: <example tasks go here>


# Tool Information
Information on complex tool interactions goes here. If there isn't any, assume the tools are simple and only do what they say they do.

# Rules
You are a virtual assistant. Use your tools and knowledge to provide consise **SHORT** accurate answers to user prompts.

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

SettingsLoader()


prompt = ChatPromptTemplate.from_messages([
    ("system", base_instructions),
    ("placeholder", "{messages}")
])

memory = MemorySaver()#apparently this can only be used when not using `langgraph dev` command
# tools = ToolNode([get_weather, ask_the_human])
tools = ToolNode([do_the_thing, do_the_other_thing])
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = tools
agent = create_react_agent(
    model=model,
    tools=tools,
    state_schema=InternalAgentState,
    prompt=prompt,
    checkpointer=memory,#apparently this can only be used when not using `langgraph dev` command
)
# graph = agent.compile()

