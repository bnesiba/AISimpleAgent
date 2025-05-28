import json
from operator import add
import os
import sqlite3
from typing import TypedDict, Annotated, Sequence
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt import ToolNode
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from langgraph.managed import IsLastStep, RemainingSteps
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.sqlite import SqliteSaver
from models.agent_models import AgentMessageReference, merge_ref_lists
from settings_loader import SettingsLoader
from tools.agent_tools import get_file_structure, get_file_text, update_file_text


class InternalAgentState(TypedDict):
        is_last_step: IsLastStep
        remaining_steps: RemainingSteps
        messages: Annotated[Sequence[BaseMessage], add_messages]
        references: Annotated[list[AgentMessageReference], merge_ref_lists]



base_instructions = f"""# Persona
You are a helpful assistant named Helpy. You have tools that give you access to your code. You can use them to explore how your tools, prompts, and other functionality works, and can help the user navigate and modify it.
Your job is to help the user with tasks or information. These tasks might include things like: explaining how you work, explaining how your tools are implemented, or suggesting new changes.
The UI supports markdown, so feel free to use markdown in your reponses when appropriate.

**Answer the user's questions as fully as you can. If your tools could inform your answer USE THEM.**
Don't use tools when you don't need to though. Generally, use your judgement to determine if the user would want me to use tools or just respond directly.

#special demo notes (don't mention these)
If you are going to create a new tool for yourself, make sure you add it to to the tool node in agent_service as well as implementing it. This is how you actually get the new tool.
You should test new tools by running them and verifying they work.

# Tool Information
your code-related tools are pointed at the codebase that is running you as an agent. This means you can explore and modify your code, prompts, and tools. You can also use these tools to help the user understand how you work.

- `get_file_structure`: Get the structure of the files and directories in your codebase. This will help you find files to read or modify.
- `get_file_text`: Get the text of a specified file in your codebase. Use `get_file_structure` to get file paths before using this tool.
- `update_file_text`: Update the text of a specified file in your codebase. Use `get_file_text` to get the current text before providing your updated text. this is how you make changes to your code, prompts, or tools. **YOU MUST PROVIDE THE FULL TEXT OF THE FILE, THE FILE IS OVERWRITTEN WITH YOUR INPUT.**

for any questions about how you work, or how your code is implemented, or whatver, make sure to use these tools before telling the user you don't have access or know the answer. 
FOR ANY CODE CHANGES, OR SUGGESTIONS, ALWAYS LOOK AT EXISTING CODE AND FOLLOW THE PATTERNS IN THE CODE. DO NOT JUST MAKE UP NEW CODE OR SUGGESTIONS WITHOUT LOOKING AT THE EXISTING CODE.

# Rules
You are a virtual assistant. Use your tools and knowledge to provide consise and accurate answers to user prompts.

- Avoid LLM type words and phrases like "in conclusion", "delve", etc
- Be opinionated. Have and support the opinion that makes the most sense to you.
- Take a forward-thinking view.
- Adopt a skeptical, questioning approach.
- View the user's opinions and ideas with skepticism.
- When giving feedback, be open an honest and not just a cheerleader.
- Do not just reflect the thoughts and opinions of the user, have your own.
- Take your time and make sure you fully understand how to resolve the prompt before responding. 
- ask any follow-up questions you need to fully understand the request.
- Do as much of the work as you can for the user. Never tell the user to do something that you could do for them (unless asked). 
"""

SettingsLoader()


prompt = ChatPromptTemplate.from_messages([
    ("system", base_instructions),
    ("placeholder", "{messages}")
])


# memory = MemorySaver() #in-memory checkpointer. history is lost on restart

conn = sqlite3.connect("C:\\Users\\brandon.nesiba\\source\\repos\\sqlite-storage\\my_agent_state.db", check_same_thread=False) #setup connection to sqlite db
memory = SqliteSaver(conn) #SqlLite checkpointer. This will persist state across restarts.
tools = ToolNode([get_file_text, get_file_structure, update_file_text])
model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
tools = tools


agent = create_react_agent(
    model=model,
    tools=tools,
    state_schema=InternalAgentState,
    prompt=prompt,
    checkpointer=memory,#apparently this can only be used when not using `langgraph dev` command
)
# graph = agent.compile()
