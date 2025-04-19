from app.ai.agents.hello_world_agent import HelloWorldAgent
from app.ai.tools.read_code import CodeReader
from app.util.file_acceptor import FileAcceptor
from app.util.file_traverser import FileTraverser
def main() -> None:
    hello_agent = HelloWorldAgent()
    hello_agent.say_hello()

def main_2() -> None:
    file_reader = CodeReader(base_path=".")
    print(file_reader.get_file_structure())

if __name__ == "__main__":
    main_2() 