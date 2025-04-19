import json
from fastmcp import FastMCP

from app.ai.tools.read_code import CodeReader
from app.ai.agents.code_location_agent import CodeLocationAgent

mcp: FastMCP = FastMCP("Code Oracle MCP")
"""
FastMCP server instance for Code Oracle.

The FastMCP server handles connections, protocol details, and message routing for MCP clients.
It exposes tools that allow Language Models to interact with code repositories.

Parameters:
    name (str): The name of the MCP server, displayed to users in Claude Desktop.
"""

@mcp.tool()
def answer_codebase_question(base_path: str, question: str) -> str:
    """
    Answer a question about the codebase by locating relevant code.
    
    This tool uses a CodeLocationAgent to analyze a codebase at the specified path
    and answer natural language questions about the code. The agent reads and processes
    the code files to provide contextually relevant answers.
    
    Parameters:
        base_path (str): The root directory path of the codebase to analyze.
        question (str): A natural language question about the codebase.
        
    Returns:
        str: A JSON string containing the answer to the question, with relevant file 
             references if applicable.
    """
    code_reader = CodeReader(base_path)
    code_location_agent = CodeLocationAgent(code_reader=code_reader)
    answer = code_location_agent.answer_question(question)
    answer_dict = {
        "answer": answer,
    }
    return json.dumps(answer_dict)

if __name__ == "__main__":
    mcp.run()