import os
import logging
from datetime import datetime
import sys

def setup_logger(name: str) -> logging.Logger:
    """
    Configures and returns a logger with the given name.

    Args:
        name (str): Name of the logger

    Returns:
        logging.Logger: Configured logger
    """
    # Create the logs directory if it doesn't exist
    log_directory = '../logs'  # Adjust this path as necessary
    os.makedirs(log_directory, exist_ok=True)

    # Log filename with the current date
    log_filename = os.path.join(log_directory, f"api_{datetime.now().strftime('%Y%m%d')}.log")

    # Configure log formatting
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File handler
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Configure logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Remove existing handlers (if any)
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger