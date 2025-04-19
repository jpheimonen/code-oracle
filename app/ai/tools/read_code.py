import json
from typing import Dict, List, Callable, Any
from pathlib import Path
from langchain_core.tools import Tool, BaseTool

from langchain_core.tools import tool

from app.util.file_traverser import FileTraverser


class CodeReader:
    def __init__(self, base_path: str):
        """
        Initialize the CodeReader with a base path.
        
        Args:
            base_path: The base path to read files from
        """
        self.base_path = Path(base_path)
        self.file_paths: List[Path] = []
        self._build_file_list()
    
    def _build_file_list(self) -> None:
        """Build a list of files using FileTraverser."""
        traverser = FileTraverser(str(self.base_path))
        self.file_paths = list(traverser)
    
    def get_file_structure(self, indices: List[int] | None = None) -> str:
        """
        Get a string representation of the file structure with indices.
        
        Args:
            indices: Optional list of indices to include in the structure. If None, include all files.
            
        Returns:
            A string representation of the file structure
        """
        result = []
        for i, file_path in enumerate(self.file_paths):
            # Skip files with indices not in the provided list
            if indices is not None and i not in indices:
                continue
                
            relative_path = file_path.relative_to(self.base_path)
            
            # Get file size with appropriate units
            size_bytes = file_path.stat().st_size
            if size_bytes < 1024:
                size_str = f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                size_str = f"{size_bytes / 1024:.1f} KB"
            elif size_bytes < 1024 * 1024 * 1024:
                size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
            else:
                size_str = f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
            
            result.append(f"[{i}] {relative_path} ({size_str})")
        
        return "\n".join(result)
    
    def get_tools(self) -> List[BaseTool]:
        """
        Get the tools provided by this class.
        
        Returns:
            A list of tool functions
        """
        @tool
        def read_code(indices: List[int]) -> str:
            """
            Read code files by their indices.
            
            Args:
                indices: A list of file indices to read
            
            Returns:
                The contents of the specified files with their paths and indices
            """
            result = []
            
            for index in indices:
                if 0 <= index < len(self.file_paths):
                    file_path = self.file_paths[index]
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        relative_path = file_path.relative_to(self.base_path)
                        result.append(f'<file path="{relative_path}" index="{index}">\n{content}\n</file>')
                    except Exception as e:
                        result.append(f'<file path="{file_path.relative_to(self.base_path)}" index="{index}">\nError reading file: {e}\n</file>')
                else:
                    result.append(f'<error>Invalid index: {index}</error>')
            
            return "\n\n".join(result)
        
        return [read_code]
