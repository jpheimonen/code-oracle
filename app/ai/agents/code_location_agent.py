from langchain_core.tools import Tool
from app.ai.agent_core.base_agent import BaseAgent
from app.ai.tools.hello_world import hello_world
from app.ai.tools.read_code import CodeReader



class CodeLocationAgent(BaseAgent):
    
    def __init__(self, code_reader: CodeReader, max_iterations: int = 10):
      super().__init__(codebase=code_reader.get_file_structure())
      self.code_reader = code_reader
      self.max_iterations = max_iterations

    def answer_question(self, question: str) -> str:
        return self.get_structured_response(question, CodeLocationAnswer)
    
    def create_tools(self) -> list[Tool]:
        return self.code_reader.get_tools()

def main():
    code_reader = CodeReader(base_path=".")
    agent = CodeLocationAgent(code_reader)
    agent.say_hello()

if __name__ == "__main__":
    main()
