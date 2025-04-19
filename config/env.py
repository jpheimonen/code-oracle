import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define typed environment dictionary
env_config: Dict[str, Any] = {
    "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY", ""),
    "azure_storage_connection_string": os.environ.get("AZURE_STORAGE_CONNECTION_STRING", ""),
    "azure_storage_container_name": os.environ.get("AZURE_STORAGE_CONTAINER_NAME", ""),
    # Azure AI Foundry configurations
    "azure_api_key": os.environ.get("AZURE_API_KEY", ""),
    "azure_api_version": os.environ.get("AZURE_API_VERSION", "2024-04-01-preview"),
    "azure_endpoint": os.environ.get("AZURE_ENDPOINT", ""),
    "azure_o3_mini_deployment": os.environ.get("AZURE_O3_MINI_DEPLOYMENT", "o3-mini")
}

# Function to validate required environment variables
def validate_env_config() -> None:
    """Validate that all required environment variables are set."""
    if not env_config["anthropic_api_key"]:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required but not set")
    if not env_config["azure_storage_connection_string"]:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is required but not set")
    if not env_config["azure_storage_container_name"]:
        raise ValueError("AZURE_STORAGE_CONTAINER_NAME environment variable is required but not set")
    
    # Only validate Azure AI if using those models (optional for now)
    # if not env_config["azure_api_key"]:
    #     raise ValueError("AZURE_API_KEY environment variable is required but not set")
    # if not env_config["azure_endpoint"]:
    #     raise ValueError("AZURE_ENDPOINT environment variable is required but not set")

# Validate environment configuration on import
validate_env_config()
