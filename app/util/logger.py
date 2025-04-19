import logging
import sys
from typing import Dict

# Cache for loggers
_loggers: Dict[str, logging.Logger] = {}
_initialized = False


def _initialize_logging() -> None:
    """Initialize the global logging configuration."""
    global _initialized
    if _initialized:
        return
    
    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.ERROR)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.ERROR)
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to root logger
    root_logger.addHandler(console_handler)
    
    _initialized = True


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name.
    
    Args:
        name: The name for the logger, typically the module name
        
    Returns:
        A configured logger instance
    """
    if name not in _loggers:
        # Initialize logging configuration if not done yet
        _initialize_logging()
        
        # Create and store the logger
        logger = logging.getLogger(name)
        _loggers[name] = logger
    
    return _loggers[name]
