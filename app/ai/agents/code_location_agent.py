from langchain_core.tools import Tool
from pydantic import BaseModel, Field
from typing import List
from app.ai.agent_core.base_agent import BaseAgent
from app.ai.tools.read_code import CodeReader
from app.util.logger import get_logger

logger = get_logger(__name__)

class RelevantFiles(BaseModel):
    relevant_files: List[int] = Field(description="List of relevant file indices that further AI agents should read. Must NOT be empty")



class CodeLocationAgent(BaseAgent):
    
    def __init__(self, code_reader: CodeReader, max_iterations: int = 10):
      super().__init__(codebase=code_reader.get_file_structure())
      self.code_reader = code_reader
      self.max_iterations = max_iterations

    def answer_question(self, question: str) -> str:
        answer = self.get_response_text(question)
        relevant_files_question = f"{self.code_reader.get_file_structure()} List indices of all files that are relevant to the answer, esp the ones you referred to in your answer: {answer}"
        relevant_files = self.get_structured_response(relevant_files_question, RelevantFiles).relevant_files

        return f"{answer}\n\nRelevant files:\n{self.code_reader.get_file_structure(relevant_files)}"
    
    def create_tools(self) -> list[Tool]:
        return self.code_reader.get_tools() # type: ignore
