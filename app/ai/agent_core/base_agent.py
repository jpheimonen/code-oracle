from abc import ABC
from typing import AsyncGenerator, Type, TypeVar
from langchain_core.tools import Tool
from pydantic import BaseModel

from app.ai.agent_core.langchain_service import LangChainService
from app.ai.prompt_loader import PromptLoader

prompt_loader = PromptLoader()

T = TypeVar('T', bound=BaseModel)

class BaseAgent(ABC):
    def __init__(self, **kwargs) -> None:
        print("Initializing BaseAgent")
        system_prompt = self._get_system_prompt(**kwargs)
        print(system_prompt)
        self.langchain_service = LangChainService(system_prompt, thinking=self.is_thinking())
        
    def is_thinking(self) -> bool:
        return True
         
    def on_user_input(self, user_input: str):
        tools = self.create_tools()
        return self.langchain_service.execute(user_input, tools)

    def on_user_input_stream(self, user_input: str) -> AsyncGenerator[dict, None]:
        tools = self.create_tools()
        return self.langchain_service.execute_stream(user_input, tools)
   

    def get_response_text(self, prompt: str) -> str:
        response = self.on_user_input(prompt)
        text = extract_step_content(response[-1])
        return text
    
    def get_structured_response(self, prompt: str, output_schema: Type[T]) -> T:
        response = self.langchain_service.get_structured_response(prompt, output_schema)
        print(response)
        return response #type: ignore

    def create_tools(self) -> list[Tool]:
        return [] # type: ignore

    def _get_prompt(self, prompt_name: str, **kwargs) -> str:
        return prompt_loader.get_prompt(self.__class__.__name__ + "_" + prompt_name, **kwargs)
    
    def _get_system_prompt(self, **kwargs) -> str:
                
        return self._get_prompt("system_prompt", **kwargs)
    

def extract_step_content(msg):
    if hasattr(msg, "name") and msg.name is not None:
        print(f"🛠️ :{msg.content}")
    elif isinstance(msg.content, list):
        for item in msg.content:
            if item.get("type") == "text":
                return item.get('text')
            elif item.get("type") == "thinking":
                return item.get('thinking')
            elif item.get("type") == "tool_use":
                return item.get('name')    

                
            else:
                return item
    elif hasattr(msg, "response_metadata") and msg.response_metadata.get('model') is not None:
        return msg.content
    else:
        return msg.content
