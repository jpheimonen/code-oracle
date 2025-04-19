from app.ai.agents.code_location_agent import CodeLocationAgent
from app.ai.tools.read_code import CodeReader
from app.util.file_acceptor import FileAcceptor
from app.util.file_traverser import FileTraverser
def main() -> None:
    code_location_agent = CodeLocationAgent(code_reader=CodeReader(base_path="."))
    print(code_location_agent.answer_question("What is the main function in the code?"))

def main_2() -> None:
    file_reader = CodeReader(base_path=".")
    print(file_reader.get_file_structure())

if __name__ == "__main__":
    main() 