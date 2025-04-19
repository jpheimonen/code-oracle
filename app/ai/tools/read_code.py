import json
from langchain_core.tools import tool

@tool
def hello_world() -> str:
    """
    This tool is used to say hello world secret hello world msg.
    """
    try:
        return "Morjesta poytaan!"
    except Exception as e:
        return f"Error: {e}"
