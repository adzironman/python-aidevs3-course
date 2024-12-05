import os
import logging
from datetime import datetime
import sys
from colorama import Fore, Style, init

# Initialize colorama
init()

class CustomFormatter(logging.Formatter):
    # Define color schemes for different logging levels
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }

    # Color for the logger name
    NAME_COLOR = Fore.CYAN

    EMOJIS = {
        "INFO": "ℹ️",
        "WARNING": "⚠️",
        "ERROR": "❌",
        "DEBUG": "🐛",
        "CRITICAL": "💀"
    }

    def format(self, record):
        # Get the color for this log level
        color = self.COLORS.get(record.levelname, '')
        
        # Add emoji to the record
        record.emoji = self.EMOJIS.get(record.levelname, "")
        
        # Color the name
        record.name = f"{self.NAME_COLOR}{record.name}{Style.RESET_ALL}"
        
        # Color the levelname and message
        if color:
            record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
            record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
        
        return super().format(record)


def setup_logger(name: str) -> logging.Logger:
    """
    Configures and returns a logger with the given name.

    Args:
        name (str): Name of the logger

    Returns:
        logging.Logger: Configured logger
    """

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(CustomFormatter(fmt="[%(name)s] - %(levelname)s: %(message)s %(emoji)s"))

    # Configure logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Remove existing handlers (if any)
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger

