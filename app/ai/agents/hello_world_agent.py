from langchain_core.tools import Tool
from app.ai.agent_core.base_agent import BaseAgent
from app.ai.tools.hello_world import hello_world
class HelloWorldAgent(BaseAgent):
    
    def __init__(self):
      super().__init__()

    def say_hello(self) -> str:
        return self.get_response_text("Say hello")
    
    def create_tools(self) -> list[Tool]:
        return []

def main():
    agent = HelloWorldAgent()
    agent.say_hello()

if __name__ == "__main__":
    main()
