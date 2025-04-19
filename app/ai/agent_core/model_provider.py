from abc import ABC, abstractmethod
from typing import Dict, Any
from config.env import env_config
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

class ModelProvider(ABC):
    @staticmethod
    def getInstance(model_type: str = "gemini-2-5-flash") -> "ModelProvider":
        """Factory method to get the appropriate model provider instance."""
        if model_type == "anthropic-claude-3-7":
            return AnthropicClaude3_7ModelProvider()
        elif model_type == "gemini-2-5-flash":
            return GeminiFlashModelProvider()
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

class GeminiFlashModelProvider(ModelProvider):
    def get_model_config(self, thinking: bool = True) -> Dict[str, Any]:
        """Return Gemini 2.5 Flash configuration."""
        return {
            "model": "gemini-2.5-flash-preview-04-17",
            "api_key": env_config["gemini_api_key"],
            "temperature": 0.7,
            "max_output_tokens": 8192,
            # Additional configs needed for proper tool calling
            "convert_system_message_to_human": True,
            # Set a lower temperature for better tool calling behavior
            "temperature": 0.1,
         #   "thinking_config": {"thinking_budget": 4096, "thinking_enabled": True} if thinking else None
        }
    
    def get_cache_control(self) -> Dict[str, Any]:
        """Return Gemini 2.5 Flash specific cache control settings."""
        return {"type": "context_cache_enabled"}
    
    def get_model(self, thinking: bool = True) -> ChatGoogleGenerativeAI:
        """Return a configured ChatGoogleGenerativeAI instance."""
        return ChatGoogleGenerativeAI(**self.get_model_config(thinking))

