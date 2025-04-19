from collections.abc import AsyncGenerator
from typing import Type, List, Any, Dict, Optional, TypeVar
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import Tool
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel
from app.ai.agent_core.model_provider import ModelProvider
from dotenv import load_dotenv
import json

DEBUG = True    
if DEBUG:
    from langchain.globals import set_debug
    set_debug(True)
load_dotenv()
config = RunnableConfig(recursion_limit=100)


T = TypeVar('T', bound=BaseModel)

class LangChainService:
    def __init__(self, system_prompt: str, thinking: bool = True, model_type: str = "gemini-2-5-flash"):
        model_provider = ModelProvider.getInstance(model_type)
        self.model = model_provider.get_model(thinking)
        self.model_type = model_type
        
        self.system_prompt = system_prompt
        self.messages = [SystemMessage(content=[{
            "type": "text",
            "text": self.system_prompt,
            "cache_control": model_provider.get_cache_control(),
        }])]

    def create_executor(self, tools: list[Tool]):
        # Add special handling for Gemini models
        if self.model_type == "gemini-2-5-flash":
            # For Gemini, bind tools directly to the model first
            bound_model = self.model.bind_tools(tools, tool_choice="auto")
            return create_react_agent(bound_model, tools)
        else:
            return create_react_agent(self.model, tools)

    def _process_gemini_tool_calls(self, msg: Any) -> None:
        """Process Gemini tool calls from additional_kwargs and add them to standard tool_calls."""
        if self.model_type == "gemini-2-5-flash" and hasattr(msg, "additional_kwargs"):
            tool_calls = msg.additional_kwargs.get("tool_calls", [])
            if tool_calls and not msg.tool_calls:
                # Copy tool calls from additional_kwargs to the standard tool_calls field
                for tc in tool_calls:
                    if tc.get("type") == "function" and tc.get("function"):
                        try:
                            args = json.loads(tc["function"].get("arguments", "{}"))
                        except:
                            args = tc["function"].get("arguments", "{}")
                            
                        msg.tool_calls.append({
                            "id": tc.get("id", ""),
                            "type": "function",
                            "name": tc["function"].get("name", ""),
                            "args": args
                        })

    def execute(self, input: str, tools: list[Tool] = []) -> List[Any]:
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
            
            # Handle Gemini tool calls
            self._process_gemini_tool_calls(msg)
            
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
            
            # Handle Gemini tool calls
            self._process_gemini_tool_calls(msg)
                            
            yield msg
            pretty_print_step(msg)    

    def get_structured_response(self, input: str, output_schema: Type[T]) -> T:
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
        print(f"🤖: {msg.content}")

