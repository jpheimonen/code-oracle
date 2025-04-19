from abc import ABC, abstractmethod
from typing import Dict, Any
from config.env import env_config
from langchain_anthropic import ChatAnthropic

class ModelProvider(ABC):
    @staticmethod
    def getInstance(model_type: str = "anthropic-claude-3-7") -> "ModelProvider":
        """Factory method to get the appropriate model provider instance."""
        if model_type == "anthropic-claude-3-7":
            return AnthropicClaude3_7ModelProvider()
        elif model_type == "azure-o3-mini":
            return AzureAIO3MiniModelProvider()
        # Add other model providers here as needed
        raise ValueError(f"Unknown model type: {model_type}")
    
    @abstractmethod
    def get_model_config(self, thinking: bool = True) -> Dict[str, Any]:
        """Return model configuration parameters."""
        pass
    
    @abstractmethod
    def get_cache_control(self) -> Dict[str, Any]:
        """Return model-specific cache control settings."""
        pass

    @abstractmethod
    def get_model(self, thinking: bool = True) -> Any:
        """Return the configured model instance."""
        pass

class AnthropicClaude3_7ModelProvider(ModelProvider):
    def get_model_config(self, thinking: bool = True) -> Dict[str, Any]:
        """Return Anthropic Claude 3.7 configuration."""
        return {
            "model_name": "claude-3-7-sonnet-20250219", 
            "anthropic_api_key": env_config["anthropic_api_key"],
            "thinking": {"budget_tokens": 4096, "type": "enabled"} if thinking else None,
            "max_tokens": 8192,
            "extra_headers": {"anthropic-beta": "prompt-caching-2024-07-31"}
        }
    
    def get_cache_control(self) -> Dict[str, Any]:
        """Return Claude 3.7 specific cache control settings."""
        return {"type": "ephemeral"}
    
    def get_model(self, thinking: bool = True) -> ChatAnthropic:
        """Return a configured ChatAnthropic instance."""
        return ChatAnthropic(**self.get_model_config(thinking))

