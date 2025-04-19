import os
from typing import Iterator, Optional
from pathlib import Path

from app.util.file_acceptor import FileAcceptor


class FileTraverser:
    def __init__(
        self,
        root_dir: str,
        acceptor=None,
        charset: str = "utf-8"
    ):
        """
        Initialize the FileTraverser.

        Args:
            root_dir: Root directory to start traversal from
            acceptor: File acceptor instance for filtering files (defaults to FileAcceptor if None)
            charset: Character encoding for reading files (default: utf-8)
        """
        self.root_dir = Path(root_dir)
        self.charset = charset
        self.acceptor = acceptor if acceptor is not None else FileAcceptor(root_dir)

    def _read_file_content(self, file_path: Path) -> Optional[str]:
        """Read file content with specified charset."""
        try:
            with open(file_path, 'r', encoding=self.charset) as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None

    def __iter__(self) -> Iterator[Path]:
        """Iterate over files based on acceptor rules."""
        for root, dirs, files in os.walk(self.root_dir):
            # Remove directories that shouldn't be traversed
            if self.acceptor:
                dirs[:] = [d for d in dirs if self.acceptor.accept_directory(Path(root) / d)]
            
            for file in files:
                file_path = Path(root) / file
                if not self.acceptor or self.acceptor.accept_file(file_path):
                    yield file_path
