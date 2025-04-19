from collections.abc import AsyncGenerator
import os
from typing import Type
from anthropic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import Tool
from langchain_core.runnables import RunnableConfig
from dotenv import load_dotenv
# from langchain.globals import set_debug
# set_debug(True)
load_dotenv()
config = RunnableConfig(recursion_limit=100)
class LangChainService:
    def __init__(self, system_prompt: str, thinking: bool = True):
        self.model = ChatAnthropic( # type: ignore
            model_name="claude-3-7-sonnet-20250219", 
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            thinking={"budget_tokens": 4096, "type":"enabled"} if thinking else None,
            max_tokens=32000,
            extra_headers={"anthropic-beta": "prompt-caching-2024-07-31,output-128k-2025-02-19"}

        )
        self.system_prompt = system_prompt
        self.messages = [SystemMessage(content=[{
            "type": "text",
            "text": self.system_prompt,
            "cache_control": { "type": "ephemeral" },
        }])]

    def create_executor(self, tools: list[Tool]):
        return create_react_agent(self.model, tools)

    def execute(self, input: str, tools: list[Tool] = []) -> None:
        agent = self.create_executor(tools)
        self.messages.append(HumanMessage(content=input)) # type: ignore
        # Run the agent with proper message formatting
        steps = []
        for step in agent.stream(
            {"messages": self.messages},
            stream_mode="values",
            config=config
        ):
            msg = step["messages"][-1]
            self.messages.append(msg)
            steps.append(msg)
            pretty_print_step(msg)
        return steps # type: ignore

    async def execute_stream(self, user_input: str, tools: list[Tool] = []) -> AsyncGenerator[dict, None]:
        agent = self.create_executor(tools)
        self.messages.append(HumanMessage(content=user_input)) # type: ignore
        for step in agent.stream(
            {"messages": self.messages},
            stream_mode="values",
            config=config
        ):
            msg = step["messages"][-1]
            self.messages.append(msg)
            yield msg
            pretty_print_step(msg)    

    def get_structured_response(self, input: str, output_schema: Type[BaseModel]) -> BaseModel:
        model_with_tools = self.model.with_structured_output(output_schema)
        return model_with_tools.invoke(input) # type: ignore
        
def pretty_print_step(msg):
    if hasattr(msg, "name") and msg.name is not None:
        print(f"🛠️ :{msg.content}")
    elif isinstance(msg.content, list):
        for item in msg.content:
            if item.get("type") == "text":
                print(f"🤖: {item.get('text')}")
            elif item.get("type") == "thinking":
                print(f"💭: {item.get('thinking')}")
            elif item.get("type") == "tool_use":
                print(f"<{item.get('name')}>\n")
                for key, value in item.get("input", {}).items():
                    print(f"<{key}>")
                    print(f"{value}")
                    print(f"</{key}>")
                print(f"</{item.get('name')}>")    

                
            else:
                print(item)
    elif hasattr(msg, "response_metadata") and msg.response_metadata.get('model') is not None:
        print(f"🤖:{msg.content}")
    else:
        print(f"👤: {msg.content}")

