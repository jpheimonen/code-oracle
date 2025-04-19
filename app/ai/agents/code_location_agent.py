from langchain_core.tools import Tool
from pydantic import BaseModel, Field
from typing import Optional, List
from app.ai.agent_core.base_agent import BaseAgent
from app.ai.tools.read_code import CodeReader


class CodeLocationAnswer(BaseModel):
    final_answer: bool = Field(description="Whether this is the final answer")
    answer: Optional[str] = Field(None, description="The answer text, required if final_answer is True")
    relevant_files: Optional[List[int]] = Field(None, description="List of relevant file indices, required if final_answer is True")

class CodeLocationAnswerFinalRequired(BaseModel):
    answer: str = Field(description="The answer text")
    relevant_files: List[int] = Field(description="List of relevant file indices")

class RelevantFiles(BaseModel):
    relevant_files: List[int] = Field(description="List of relevant file indices that further AI agents should read")



class CodeLocationAgent(BaseAgent):
    
    def __init__(self, code_reader: CodeReader, max_iterations: int = 10):
      super().__init__(codebase=code_reader.get_file_structure())
      self.code_reader = code_reader
      self.max_iterations = max_iterations

    def answer_question(self, question: str) -> str:
        answer = self.get_response_text(question)
        relevant_files = self.get_structured_response(question, RelevantFiles).relevant_files
        print(relevant_files)

        return f"{answer}\nRelevant files: {self.code_reader.get_file_structure(relevant_files)}"
    
    def answer_question_old(self, question: str) -> str:
        answer = CodeLocationAnswer(final_answer=False, answer=None, relevant_files=None)
        count = 0
        while not answer.final_answer and count < self.max_iterations-1:
            answer = self.get_structured_response(question, CodeLocationAnswer)
            count += 1

        if answer.final_answer:
            final_answer = self.get_structured_response(question, CodeLocationAnswerFinalRequired)
            return final_answer.answer
        else:
            return answer.answer # type: ignore
        
    
    def create_tools(self) -> list[Tool]:
        return self.code_reader.get_tools() # type: ignore

def main():
    code_reader = CodeReader(base_path=".")
    agent = CodeLocationAgent(code_reader)
    agent.say_hello()

if __name__ == "__main__":
    main()
