from app.ai.agents.hello_world_agent import HelloWorldAgent
from app.util.file_acceptor import FileAcceptor
from app.util.file_traverser import FileTraverser
def main() -> None:
    hello_agent = HelloWorldAgent()
    hello_agent.say_hello()

def main_2() -> None:
    file_traverser = FileTraverser(root_dir=".", acceptor=FileAcceptor(root_dir="."))
    for file in file_traverser:
        print(file)

if __name__ == "__main__":
    main_2() 