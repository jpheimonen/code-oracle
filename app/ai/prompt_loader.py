import os
from typing import Dict, Any
from pathlib import Path

class PromptLoader:
    def __init__(self, prompts_dir: str = "app/static_prompts"):
        self.prompts_dir = prompts_dir
        self._prompts_cache: Dict[str, str] = {}

    def get_prompt(self, prompt_name: str, **kwargs) -> str:
        """
        Load a prompt from markdown file and format it with provided kwargs
        
        Args:
            prompt_name: Name of the prompt file without .md extension
            **kwargs: Variables to format the prompt with
            
        Returns:
            Formatted prompt string
        """
        print(f"Loading prompt {prompt_name}")
        if prompt_name not in self._prompts_cache:
            print(f"Prompt {prompt_name} not in cache")
            prompt_path = os.path.join(self.prompts_dir, f"{prompt_name}.md")
            print(f"Prompt path: {prompt_path}")
            if not os.path.exists(prompt_path):
                print(f"Prompt file {prompt_path} not found")
                raise FileNotFoundError(f"Prompt file {prompt_path} not found")
            print(f"Prompt file {prompt_path} found")
            try:
                with open(prompt_path, 'r') as f:
                    self._prompts_cache[prompt_name] = f.read().strip()
            except Exception as e:
                print(f"Error reading prompt file {prompt_path}: {e}")
                raise e
        print(f"Loaded prompt {prompt_name}")
        prompt_template = self._prompts_cache[prompt_name]
        print(f"Formatting prompt {prompt_name}")
        try:
            return prompt_template.format(**kwargs)
        except KeyError as e:
            missing_key = str(e).strip("'")
            raise KeyError(f"Missing required variable '{missing_key}' for prompt '{prompt_name}'") 