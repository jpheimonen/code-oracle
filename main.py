from app.ai.agents.code_location_agent import CodeLocationAgent
from app.ai.tools.read_code import CodeReader
from app.util.file_acceptor import FileAcceptor
from app.util.file_traverser import FileTraverser
import sys
    
def main() -> None:
    
    code_location_agent = CodeLocationAgent(code_reader=CodeReader(base_path="."))
    
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = input("Enter your question about the codebase: ")
    
    print(code_location_agent.answer_question(question))
def main_2() -> None:
    file_reader = CodeReader(base_path=".")
    print(file_reader.get_file_structure())

if __name__ == "__main__":
    main() 