from app.ai.agents.code_location_agent import CodeLocationAgent
from app.ai.tools.read_code import CodeReader
from app.util.file_acceptor import FileAcceptor
from app.util.file_traverser import FileTraverser
import sys
    
def main() -> None:
    base_path = sys.argv[1] if len(sys.argv) > 1 else "."
    code_reader = CodeReader(base_path)
    print(code_reader.get_file_structure())
    code_location_agent = CodeLocationAgent(code_reader=code_reader)
    
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = input("Enter your question about the codebase: ")
    
    print(code_location_agent.answer_question(question))

if __name__ == "__main__":
    main() 