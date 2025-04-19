import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define typed environment dictionary
env_config: Dict[str, Any] = {
    "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY", ""),
    # Google API configurations
    "gemini_api_key": os.environ.get("GEMINI_API_KEY", "")
}

# Function to validate required environment variables
def validate_env_config() -> None:
    """Validate that all required environment variables are set."""
    if not env_config["gemini_api_key"]:
        raise ValueError("GEMINI_API_KEY environment variable is required but not set")

# Validate environment configuration on import
validate_env_config()
