import os
from pathlib import Path
from typing import List, Set, Optional
import fnmatch
import warnings


class FileAcceptor:
    """
    Class to determine which files should be accepted during traversal.
    Handles gitignore patterns and common exclusion rules.
    """
    
    # Common binary file extensions that should be ignored
    BINARY_EXTENSIONS = {
        '.pyc', '.so', '.o', '.a', '.lib', '.dll', '.exe', '.bin', '.dat',
        '.db', '.sqlite', '.sqlite3', '.mdb', '.accdb', '.frm', '.ibd',
        '.myd', '.myi', '.dbf', '.db-shm', '.db-wal',
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.tif', '.tiff',
        '.webp', '.svg', '.psd', '.ai',
        '.mp3', '.mp4', '.wav', '.avi', '.mov', '.mkv', '.flv', '.webm',
        '.wmv', '.mpg', '.mpeg', '.m4a', '.ogg', '.flac',
        '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.tgz',
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        '.iso', '.dmg', '.img',
        '.class', '.jar', '.war', '.ear', '.pak',
        '.woff', '.woff2', '.ttf', '.otf', '.eot',
    }
    
    # Common directories to ignore
    IGNORED_DIRS = {
        'node_modules',
        '__pycache__',
        'venv',
        'env',
        '.venv',
        '.env',
        '.git',
        '.svn',
        '.hg',
        '.idea',
        '.vscode',
        'build',
        'dist',
        'target',
        'bin',
        'obj',
    }

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.gitignore_patterns: List[str] = []
        
        # Find and load gitignore
        gitignore_path = self._find_gitignore(self.root_dir)
        if gitignore_path:
            self._load_gitignore(gitignore_path)
        else:
            warnings.warn("No .gitignore file found. All files will be processed unless explicitly ignored.")

    def _find_gitignore(self, start_dir: Path) -> Optional[Path]:
        """
        Find .gitignore file starting from start_dir and going up to root.
        
        Args:
            start_dir: Directory to start search from
            
        Returns:
            Path to .gitignore if found, None otherwise
        """
        current_dir = start_dir
        
        while current_dir != current_dir.parent:
            gitignore_path = current_dir / '.gitignore'
            if gitignore_path.exists():
                return gitignore_path
            current_dir = current_dir.parent
            
        return None

    def _load_gitignore(self, gitignore_path: Path) -> None:
        """
        Load patterns from .gitignore file.
        
        Args:
            gitignore_path: Path to .gitignore file
        """
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith('#'):
                        self.gitignore_patterns.append(line)
        except Exception as e:
            warnings.warn(f"Error reading .gitignore file: {e}")

    def _is_gitignored(self, path: Path) -> bool:
        """
        Check if path matches any gitignore pattern.
        
        Args:
            path: Path to check
            
        Returns:
            True if path is ignored, False otherwise
        """
        # Get path relative to root dir
        try:
            rel_path = path.relative_to(self.root_dir)
        except ValueError:
            # If path is not relative to root_dir, use absolute path
            rel_path = path
        
        rel_path_str = str(rel_path).replace('\\', '/')
        
        for pattern in self.gitignore_patterns:
            # Normalize pattern
            pattern = pattern.rstrip('/')
            
            # Handle negation
            if pattern.startswith('!'):
                continue  # Skip negation patterns for simplicity
                
            # Handle directory-only patterns
            is_dir_pattern = pattern.endswith('/')
            if is_dir_pattern and not path.is_dir():
                continue
                
            # Remove trailing slash for matching
            if is_dir_pattern:
                pattern = pattern[:-1]
                
            # Handle patterns with wildcards
            if any(c in pattern for c in '*?['):
                if fnmatch.fnmatch(rel_path_str, pattern):
                    return True
                parts = rel_path_str.split('/')
                for i in range(len(parts)):
                    if fnmatch.fnmatch('/'.join(parts[:i+1]), pattern):
                        return True
            # Direct match
            elif rel_path_str == pattern or rel_path_str.startswith(pattern + '/'):
                return True
                
        return False

    def accept_file(self, file_path: Path) -> bool:
        """
        Determine if a file should be accepted.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file should be accepted, False otherwise
        """
        # Check if it's a known binary file
        if file_path.suffix.lower() in self.BINARY_EXTENSIONS:
            return False
            
        # Check if file is gitignored
        if self._is_gitignored(file_path):
            return False
            
        return True

    def accept_directory(self, dir_path: Path) -> bool:
        """
        Determine if a directory should be traversed.
        
        Args:
            dir_path: Path to the directory
            
        Returns:
            True if directory should be traversed, False otherwise
        """
        # Ignore directories that start with .
        if dir_path.name.startswith('.'):
            return False
            
        # Ignore common directories
        if dir_path.name in self.IGNORED_DIRS:
            return False
            
        # Check if directory is gitignored
        if self._is_gitignored(dir_path):
            return False
            
        return True 