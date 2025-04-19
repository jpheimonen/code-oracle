#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd $SCRIPT_DIR

# Create and activate virtual environment with uv if it doesn't exist
if [ ! -d ".venv" ]; then
    uv venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies with uv
uv pip sync

# Run the MCP server
fastmcp run mcp.py

