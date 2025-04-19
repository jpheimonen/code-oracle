from app.ai.agents.hello_world_agent import HelloWorldAgent

def main() -> None:
    hello_agent = HelloWorldAgent()
    hello_agent.say_hello()

if __name__ == "__main__":
    main() 